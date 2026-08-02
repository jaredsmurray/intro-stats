# Helpers for values inserted into prose and display equations.

#' Format a signed value without hard-coding its sign
#'
#' `formatter` receives the magnitude of `x`, so it can be any scales-style
#' formatter such as `scales::number` or `scales::comma`. The sign is chosen
#' from the value but suppressed when the formatted magnitude rounds to zero.
#' Put unit strings such as `"\\$"` in `prefix` so the sign appears first.
#'
#' @param x A finite numeric vector.
#' @param formatter A function that formats nonnegative numeric values.
#' @param ... Arguments passed to `formatter`.
#' @param prefix A string inserted between the sign and formatted magnitude.
#' @param show_plus Whether positive, nonzero values receive a leading `+`.
format_signed <- function(x,
                          formatter = scales::number,
                          ...,
                          prefix = "",
                          show_plus = TRUE) {
  if (!is.numeric(x) || any(!is.finite(x))) {
    stop("`x` must contain only finite numeric values.", call. = FALSE)
  }
  if (!is.logical(show_plus) || length(show_plus) != 1L || is.na(show_plus)) {
    stop("`show_plus` must be TRUE or FALSE.", call. = FALSE)
  }

  magnitude <- formatter(abs(x), ...)
  formatted_zero <- formatter(rep(0, length(x)), ...)
  sign <- ifelse(
    magnitude == formatted_zero,
    "",
    ifelse(x < 0, "-", if (show_plus) "+" else "")
  )

  paste0(sign, prefix, magnitude)
}

#' Format a dollar value for use inside math spans
#'
#' A bare "$" from `scales::dollar()` reads as the start of a math span, and
#' pandoc then scans to the next "$" -- swallowing everything between,
#' including table delimiters. Escape it instead, and brace the comma so
#' MathJax sets "571{,}000" rather than "571, 000" with punctuation spacing.
math_usd <- function(x, accuracy = 1) {
  paste0("\\$", gsub(",", "{,}", scales::comma(x, accuracy = accuracy), fixed = TRUE))
}
