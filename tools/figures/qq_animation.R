# ══════════════════════════════════════════════════════════════════════════════
# Standalone script: animates how QQ plots work by progressively adding quantiles.
# Compares z-scored S&P 500 weekly returns to the theoretical standard normal
# distribution. Uses a density-scaled histogram with overlaid density estimate
# (instead of count histogram) to better visualize the fit.
#
# Tied to: prob_04_normal.qmd, section "QQ plots: checking normality"
# ══════════════════════════════════════════════════════════════════════════════

library(tidyverse)
library(patchwork)
library(magick)

# Load returns data (same as in prob_04_normal.qmd)
returns <- read_csv("/Users/jm75583/Dropbox/intro_notes_revision/data/returns/returns.csv",
                    show_col_types = FALSE) |>
  mutate(date = as.Date(date))

# Z-score the S&P 500 returns
z_returns <- (returns$market - mean(returns$market)) / sd(returns$market)

# Create paired plot function with density-scaled histogram
create_paired_plot <- function(z_scores, percentiles_to_show) {

  # Get the current percentile (last one in the list)
  current_p <- percentiles_to_show[length(percentiles_to_show)]
  obs_val <- quantile(z_scores, current_p)
  theor_val <- qnorm(current_p)

  # Top left: Density-scaled histogram with overlaid density estimate
  p1a <- ggplot(tibble(x = z_scores), aes(x = x)) +
    geom_histogram(aes(y = after_stat(density)),
                   bins = 40, fill = "lightblue", color = "white") +
    geom_density(color = "darkblue", linewidth = 0.8, alpha = 0.7) +
    geom_vline(xintercept = obs_val, color = "blue", linetype = "dashed", linewidth = 1) +
    geom_segment(x = theor_val, y = 0, xend = theor_val, yend = -0.05,
                 color = "purple", linewidth = 1.5) +
    labs(title = "S&P 500 Z-Scored Returns (Observed)",
         x = NULL, y = "Density") +
    xlim(-4, 4) +
    theme_minimal(base_size = 14) +
    theme(axis.text.x = element_blank(),
          axis.ticks.x = element_blank())

  # Bottom left: Normal density with theoretical percentile line
  p1b <- ggplot(tibble(x = seq(-4, 4, length.out = 200)), aes(x = x)) +
    stat_function(fun = dnorm, color = "purple", linewidth = 1) +
    geom_vline(xintercept = theor_val, color = "purple", linetype = "dashed", linewidth = 1) +
    labs(x = paste0(round(current_p * 100, 1), "% of values are below vertical line"),
         y = "Density",
         title = "Normal Distribution (Theoretical)") +
    xlim(-4, 4) +
    theme_minimal(base_size = 14)

  # Build data for all points shown so far
  qq_points <- tibble(
    percentile = percentiles_to_show,
    theoretical = qnorm(percentiles_to_show),
    observed = quantile(z_scores, percentiles_to_show)
  ) %>%
    mutate(is_current = percentile == current_p)

  # Right panel: QQ plot
  p2 <- ggplot(qq_points, aes(x = theoretical, y = observed)) +
    geom_abline(slope = 1, intercept = 0, color = "gray50", linetype = "dashed") +
    # Add segments from axes to current point
    geom_segment(x = theor_val, y = -4, xend = theor_val, yend = obs_val,
                 color = "purple", linetype = "dashed") +
    geom_segment(x = -4, y = obs_val, xend = theor_val, yend = obs_val,
                 color = "blue", linetype = "dashed") +
    geom_point(data = filter(qq_points, !is_current),
               color = "gray60", size = 3) +
    geom_point(data = filter(qq_points, is_current),
               color = "black", size = 3.5) +
    labs(title = "QQ-Plot",
         x = "Theoretical Quantiles",
         y = "Observed Quantiles") +
    coord_fixed(ratio = 1, xlim = c(-4, 4), ylim = c(-4, 4)) +
    theme_minimal(base_size = 14)

  # Combine panels
  (p1a / p1b) | p2
}

# Helper function to render plot as image
to_image <- function(p, width = 12, height = 5, dpi = 100) {
  tmp <- tempfile(fileext = ".png")
  ggsave(tmp, p, width = width, height = height, dpi = dpi)
  image_read(tmp)
}

cat("Rendering frames...\n")

# Create animation with progressive percentiles
set.seed(235)
percentiles <- seq(0.01, 0.99, by = 0.01)

frames <- map(seq_along(percentiles), function(i) {
  to_image(create_paired_plot(z_returns, percentiles[1:i]))
})

# Add a hold frame at the end to pause on the final frame
hold_frames <- rep(list(to_image(create_paired_plot(z_returns, percentiles))), 8)
all_frames <- c(frames, hold_frames)

# Animate and save
gif <- image_join(all_frames)
gif <- image_animate(gif, fps = 10, dispose = "previous")

out_dir <- "/Users/jm75583/Dropbox/intro_notes_revision/images"
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)
out_path <- file.path(out_dir, "qq_animation.gif")
image_write(gif, out_path)
cat("Saved", out_path, "\n")
