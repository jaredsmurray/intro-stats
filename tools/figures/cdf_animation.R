library(tidyverse)
library(scales)
library(patchwork)
library(magick)

# ══════════════════════════════════════════════════════════════════════════════
# Standalone script: animates the accumulation of area under the sale-price
# density into the cumulative distribution function (CDF). The lognormal model
# is fit by method of moments to match the density construction in
# prob_02_probability-basics.qmd (chunk fig-price-model-density).
# ══════════════════════════════════════════════════════════════════════════════

austin <- read_csv("/Users/jm75583/Dropbox/data/austin_houses/austin_houses_subset.csv",
                   show_col_types = FALSE)

# Lognormal model by method of moments.
m <- mean(austin$latest_price)
v <- var(austin$latest_price)
sdlog <- sqrt(log(1 + v / m^2))
mulog <- log(m) - log(1 + v / m^2) / 2

dens_df <- tibble(x = seq(1e4, 2e6, length.out = 800),
                  y = dlnorm(x, mulog, sdlog))
cdf_df <- tibble(x = seq(1e4, 2e6, length.out = 800),
                 y = plnorm(x, mulog, sdlog))

# Fixed axis pieces so frames don't jump.
dollar_axis <- scale_x_continuous(labels = dollar_format(scale = 1e-3, suffix = "K"),
                                  limits = c(0, 2e6))
y_dens_max <- max(dens_df$y) * 1.05

# Left panel: density with the region x <= x0 shaded.
render_dens <- function(x0) {
  ggplot(dens_df, aes(x = x, y = y)) +
    geom_area(data = filter(dens_df, x <= x0),
              fill = "darkorange", alpha = 0.8) +
    geom_line(color = "steelblue", linewidth = 1) +
    dollar_axis +
    scale_y_continuous(limits = c(0, y_dens_max)) +
    labs(x = "Sale price", y = "Density") +
    theme_minimal(base_size = 10)
}

# Right panel: CDF drawn only up to x0, with a point at the running threshold.
render_cdf <- function(x0) {
  ggplot() +
    geom_line(data = filter(cdf_df, x <= x0), aes(x = x, y = y),
              color = "steelblue", linewidth = 1) +
    annotate("point", x = x0, y = plnorm(x0, mulog, sdlog),
             color = "darkorange", size = 3) +
    dollar_axis +
    scale_y_continuous(limits = c(0, 1)) +
    labs(x = "Sale price", y = "Cumulative probability") +
    theme_minimal(base_size = 10)
}

# Hold frame: completed density and full CDF, point held at the far-right end.
render_dens_full <- function() {
  ggplot(dens_df, aes(x = x, y = y)) +
    geom_area(fill = "darkorange", alpha = 0.8) +
    geom_line(color = "steelblue", linewidth = 1) +
    dollar_axis +
    scale_y_continuous(limits = c(0, y_dens_max)) +
    labs(x = "Sale price", y = "Density") +
    theme_minimal(base_size = 10)
}

render_cdf_full <- function() {
  x_end <- max(cdf_df$x)
  ggplot() +
    geom_line(data = cdf_df, aes(x = x, y = y),
              color = "steelblue", linewidth = 1) +
    annotate("point", x = x_end, y = plnorm(x_end, mulog, sdlog),
             color = "darkorange", size = 3) +
    dollar_axis +
    scale_y_continuous(limits = c(0, 1)) +
    labs(x = "Sale price", y = "Cumulative probability") +
    theme_minimal(base_size = 10)
}

to_image <- function(p, width = 9, height = 4, dpi = 100) {
  tmp <- tempfile(fileext = ".png")
  ggsave(tmp, p, width = width, height = height, dpi = dpi)
  image_read(tmp)
}

cat("Rendering frames...\n")

# Threshold x0 sweeping across the price range in ~50 evenly spaced steps.
x0_seq <- seq(1e4, 2e6, length.out = 50)

sweep_frames <- map(x0_seq, function(x0) {
  to_image(render_dens(x0) | render_cdf(x0))
})

hold_frames <- rep(list(to_image(render_dens_full() | render_cdf_full())), 8)

frames <- c(sweep_frames, hold_frames)

gif <- image_join(frames)
gif <- image_animate(gif, fps = 10, dispose = "previous")

out_dir <- "/Users/jm75583/Dropbox/intro_notes_revision/images"
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)
out_path <- file.path(out_dir, "cdf_accumulation.gif")
image_write(gif, out_path)
cat("Saved", out_path, "\n")
