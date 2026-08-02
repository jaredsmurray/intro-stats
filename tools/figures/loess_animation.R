library(tidyverse)
library(scales)
library(magick)

# ══════════════════════════════════════════════════════════════════════════════
# Standalone script: animates the windowed running-line smoother construction
# shown in twovar_02_quantitative-quantitative.qmd (chunk fig-ercot-load-temp). Keep h and the
# grid IDENTICAL to that chunk, which draws the final static version of this
# exact construction.
# ══════════════════════════════════════════════════════════════════════════════

load1 <- read_csv("/Users/jm75583/Dropbox/data/ercot/ercotproject/Data/load_1.csv",
                  show_col_types = FALSE)
load2 <- read_csv("/Users/jm75583/Dropbox/data/ercot/ercotproject/Data/load_2.csv",
                  show_col_types = FALSE)
load3 <- read_csv("/Users/jm75583/Dropbox/data/ercot/ercotproject/Data/load_3.csv",
                  show_col_types = FALSE)
ercot <- bind_rows(load1, load2, load3) |>
  filter(LOCATION == "North Central (DFW)") |>
  mutate(datetime = parse_date_time(DATEHOUR, orders = c("ymd HM", "ymd HMS")),
         year = year(datetime),
         date = as.Date(datetime)) |>
  filter(year >= 2016, year <= 2020)
rm(load1, load2, load3)

weather <- read_csv("/Users/jm75583/Dropbox/data/ercot/ercotproject/Data/weather_ncent.csv",
                    show_col_types = FALSE) |>
  mutate(datetime = parse_date_time(DATEHOUR, orders = c("ymd HM", "ymd HMS")),
         year = year(datetime)) |>
  filter(year >= 2016, year <= 2020)

ercot_temp <- ercot |>
  inner_join(weather, by = c("datetime", "LOCATION"),
             relationship = "many-to-many") |>
  filter(!is.na(HourlyDryBulbTemperature), !is.na(LOAD)) |>
  distinct(datetime, .keep_all = TRUE)
rm(weather)

ercot_daily <- ercot_temp |>
  summarize(temp = mean(HourlyDryBulbTemperature, na.rm = TRUE),
            load = mean(LOAD, na.rm = TRUE),
            .by = date)

# Windowed running-line smoother. Keep h and the grid IDENTICAL to
# twovar_02_quantitative-quantitative.qmd, chunk fig-ercot-load-temp.
h <- 8
x_grid <- seq(min(ercot_daily$temp) + h, max(ercot_daily$temp) - h, length.out = 80)

local_fit <- function(x0) {
  window <- filter(ercot_daily, abs(temp - x0) <= h)
  fit <- lm(load ~ temp, data = window)
  predict(fit, newdata = tibble(temp = x0))
}
smooth_df <- tibble(temp = x_grid, load = map_dbl(x_grid, local_fit))

# Fixed axis limits across all frames so frames don't jump.
x_limits <- range(ercot_daily$temp)
y_limits <- range(ercot_daily$load)

theme_loess <- theme_minimal()

base_plot <- function() {
  ggplot() +
    scale_x_continuous(limits = x_limits) +
    scale_y_continuous(labels = comma_format(), limits = y_limits) +
    labs(x = expression("Temperature ("*degree*"F)"), y = "Load (MW)") +
    theme_loess
}

render_frame <- function(x0) {
  window <- filter(ercot_daily, abs(temp - x0) <= h)
  fit <- lm(load ~ temp, data = window)
  y_lo <- predict(fit, newdata = tibble(temp = x0 - h))
  y_hi <- predict(fit, newdata = tibble(temp = x0 + h))
  y0 <- predict(fit, newdata = tibble(temp = x0))

  smooth_so_far <- filter(smooth_df, temp <= x0)

  p <- base_plot() +
    annotate("rect", xmin = x0 - h, xmax = x0 + h, ymin = -Inf, ymax = Inf,
             fill = "darkorange", alpha = 0.10) +
    geom_point(data = ercot_daily, aes(x = temp, y = load),
               alpha = 0.3, size = 0.8, color = "grey50") +
    geom_point(data = window, aes(x = temp, y = load),
               color = "steelblue", alpha = 0.6, size = 0.9) +
    annotate("segment", x = x0 - h, xend = x0 + h, y = y_lo, yend = y_hi,
             color = "darkorange", linewidth = 1) +
    geom_line(data = smooth_so_far, aes(x = temp, y = load),
              color = "steelblue", linewidth = 1.1) +
    annotate("point", x = x0, y = y0, color = "steelblue", size = 3)

  p
}

render_hold_frame <- function() {
  base_plot() +
    geom_point(data = ercot_daily, aes(x = temp, y = load),
               alpha = 0.3, size = 0.8, color = "grey50") +
    geom_line(data = smooth_df, aes(x = temp, y = load),
              color = "steelblue", linewidth = 1.1)
}

to_image <- function(p, width = 8, height = 5, dpi = 100) {
  tmp <- tempfile(fileext = ".png")
  ggsave(tmp, p, width = width, height = height, dpi = dpi)
  image_read(tmp)
}

cat("Rendering frames...\n")

# ~45 evenly spaced focal points, subsampled from the 80-point grid
focal_idx <- unique(round(seq(1, length(x_grid), length.out = 45)))
focal_x <- x_grid[focal_idx]

sweep_frames <- map(focal_x, function(x0) to_image(render_frame(x0)))

hold_frames <- rep(list(to_image(render_hold_frame())), 8)

frames <- c(sweep_frames, hold_frames)

gif <- image_join(frames)
gif <- image_animate(gif, fps = 10, dispose = "previous")

out_dir <- "/Users/jm75583/Dropbox/intro_notes_revision/images"
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)
out_path <- file.path(out_dir, "loess_construction.gif")
image_write(gif, out_path)
cat("Saved", out_path, "\n")
