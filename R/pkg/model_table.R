# Regression tables for the book. Two displays:
#
# reg_table()  compares several models -- one column per model, each
#              coefficient's estimate with its 95% confidence interval beneath,
#              blanks where a term is not in that model, and a bottom block of
#              fit statistics.
# coef_table() lays out a single model the way summary() does -- one row per
#              coefficient, with Estimate / SE / 95% CI / t / p-value columns,
#              and RSE, R^2, and adjusted R^2 underneath.

library(modelsummary)
library(kableExtra)

# modelsummary's goodness-of-fit list for lm() has rmse but not sigma, so add
# the residual standard error here. Registered as an S3 method on lm.
glance_custom.lm <- function(x, ...) {
  data.frame(sigma = summary(x)$sigma)
}

# Labels for the bottom block. Keys are modelsummary's raw gof names. The
# superscript is written as an escape and marked UTF-8: modelsummary runs the
# label through gsub(), which errors on a stray high byte when the session
# locale is C.
reg_table_gof_labels <- enc2utf8(c(
  sigma = "Residual standard error",
  r.squared = "R\u00b2",
  adj.r.squared = "Adjusted R\u00b2",
  nobs = "n"
))

#' Compare regression models in one table
#'
#' @param models  A named list of fitted models; the names become the column
#'   headers. A single model works too.
#' @param fmt     Number of decimal places, or a formatting function such as
#'   scales::label_dollar(accuracy = 1). Applies to the estimates and the
#'   interval endpoints alike.
#' @param coef_map Optional named character vector for renaming and reordering
#'   coefficients, e.g. c(living_area_sq_ft = "Living area (sq ft)"). Terms not
#'   named are dropped, so list every term you want shown.
#' @param gof     Which goodness-of-fit statistics to put in the bottom block,
#'   in order. Defaults to RSE, both R^2s, and n. One per row: with several
#'   model columns, a paired "0.602 / 0.600" cell reads ambiguously.
#' @param output  Passed to modelsummary(). The default renders HTML through
#'   kableExtra, matching the knitr::kable() tables elsewhere in the book; use
#'   "markdown" or "data.frame" when checking a table at the console.
#' @param ...     Passed on to modelsummary() -- notes, align, add_rows, etc.
reg_table <- function(models,
                      fmt = 2,
                      coef_map = NULL,
                      gof = c("sigma", "r.squared", "adj.r.squared", "nobs"),
                      output = "kableExtra",
                      ...) {
  if (!is.list(models)) models <- list(models)

  gof_map <- lapply(gof, function(g) {
    list(
      raw = g,
      clean = if (g %in% names(reg_table_gof_labels)) {
        unname(reg_table_gof_labels[g])
      } else {
        g
      },
      # sigma is on the response scale, so it takes the same formatting as the
      # coefficients; the unitless statistics do not. The count is grouped to
      # match coef_table().
      fmt = switch(g,
        sigma = fmt,
        nobs = function(x) formatC(x, big.mark = ",", format = "d"),
        3
      )
    )
  })

  out <- modelsummary(
    models,
    estimate = "{estimate}",
    statistic = "[{conf.low}, {conf.high}]",
    conf_level = 0.95,
    stars = FALSE,
    fmt = fmt,
    coef_map = coef_map,
    gof_map = gof_map,
    output = output,
    ...
  )

  # modelsummary pads some column headers with a literal "&nbsp;", which
  # kableExtra then escapes, so the entity shows up as text in the header
  # (e.g. "&nbsp;ZIP code only"). An escaped one is always a mistake; drop it.
  if (is.character(out)) {
    cls <- class(out)
    att <- attributes(out)
    out <- gsub("&amp;nbsp;", "", out, fixed = TRUE)
    attributes(out) <- att
    class(out) <- cls
  }

  out
}

# Apply fmt -- either a digit count or a formatting function -- to a numeric
# vector. Shared by coef_table()'s columns.
reg_format <- function(x, fmt) {
  out <- if (is.function(fmt)) fmt(x) else formatC(x, format = "f", digits = fmt)
  true_minus(out)
}

# modelsummary sets negatives with a true minus sign (U+2212), so match it here
# and the two displays agree when they sit near each other.
true_minus <- function(x) gsub("-", "−", x, fixed = TRUE)

# p-values get their own rule: three decimals, and anything smaller than 0.001
# is reported as "<0.001" rather than a string of zeros.
format_pvalue <- function(p) {
  ifelse(p < 0.001, "<0.001", formatC(p, format = "f", digits = 3))
}

#' Lay out a single model like an R summary table
#'
#' One row per coefficient, with columns for the estimate, its standard error,
#' its 95% confidence interval, the t statistic, and the p-value. Residual
#' standard error, R^2, adjusted R^2, and the sample size follow underneath.
#'
#' @param model    A fitted model.
#' @param fmt      Number of decimal places, or a formatting function such as
#'   scales::label_dollar(accuracy = 1), for the estimate, standard error, and
#'   interval columns. The t statistic and p-value always print as plain
#'   numbers.
#' @param coef_map Optional named character vector for renaming and reordering
#'   coefficients. Terms not named are dropped, so list every term you want.
#' @param gof      Which fit statistics to put underneath the coefficients. The
#'   two R^2s always share one row when both are asked for. Asking for "nobs"
#'   also reports how many rows the fit dropped, whenever that number isn't
#'   zero.
#' @param ...      Passed on to kableExtra::kbl() -- caption, align, etc.
coef_table <- function(model,
                       fmt = 2,
                       coef_map = NULL,
                       gof = c("sigma", "r.squared", "adj.r.squared", "nobs"),
                       ...) {
  est <- summary(model)$coefficients
  ci <- confint(model, level = 0.95)
  terms <- rownames(est)

  if (!is.null(coef_map)) {
    terms <- intersect(names(coef_map), terms)
    est <- est[terms, , drop = FALSE]
    ci <- ci[terms, , drop = FALSE]
    labels <- unname(coef_map[terms])
  } else {
    labels <- terms
  }

  body <- data.frame(
    Term = labels,
    Estimate = reg_format(est[, "Estimate"], fmt),
    SE = reg_format(est[, "Std. Error"], fmt),
    CI = paste0(
      "[", reg_format(ci[, 1], fmt), ", ", reg_format(ci[, 2], fmt), "]"
    ),
    t = true_minus(formatC(est[, "t value"], format = "f", digits = 2)),
    p = format_pvalue(est[, "Pr(>|t|)"]),
    check.names = FALSE
  )

  # Fit statistics go in the Estimate column, with the rest of the row blank.
  # The two R^2s share a row -- "R²/Adjusted R²" against "0.602/0.600" -- since
  # they are read together and a row each wastes the width.
  s <- summary(model)
  gof_labels <- character(0)
  gof_display <- character(0)

  if ("sigma" %in% gof) {
    gof_labels <- c(gof_labels, unname(reg_table_gof_labels["sigma"]))
    # Only sigma is on the response scale; the R^2s are unitless.
    gof_display <- c(gof_display, reg_format(s$sigma, fmt))
  }
  r2 <- intersect(c("r.squared", "adj.r.squared"), gof)
  if (length(r2) > 0) {
    values <- c(r.squared = s$r.squared, adj.r.squared = s$adj.r.squared)[r2]
    gof_labels <- c(
      gof_labels,
      paste(unname(reg_table_gof_labels[r2]), collapse = " / ")
    )
    gof_display <- c(
      gof_display,
      paste(formatC(values, format = "f", digits = 3), collapse = " / ")
    )
  }
  if ("nobs" %in% gof) {
    gof_labels <- c(gof_labels, unname(reg_table_gof_labels["nobs"]))
    gof_display <- c(gof_display, formatC(nobs(model), big.mark = ",", format = "d"))

    # lm() silently drops rows with a missing outcome or predictor, and
    # na.omit records which ones. Say so when it happened; stay quiet when the
    # fit used every row.
    dropped <- length(model$na.action)
    if (dropped > 0) {
      gof_labels <- c(gof_labels, "Rows dropped (missing values)")
      gof_display <- c(
        gof_display,
        formatC(dropped, big.mark = ",", format = "d")
      )
    }
  }

  gof_rows <- data.frame(
    Term = gof_labels,
    Estimate = gof_display,
    SE = "", CI = "", t = "", p = "",
    check.names = FALSE
  )

  tab <- rbind(body, gof_rows)
  names(tab) <- c(
    " ", "Estimate", "Std. error", "95% CI", "t", "p-value"
  )

  kbl(
    tab,
    row.names = FALSE,
    align = c("l", "r", "r", "r", "r", "r"),
    ...
  ) |>
    kable_styling(full_width = FALSE) |>
    # A rule separates the coefficients from the fit statistics.
    # A rule separates the coefficients from the fit statistics, matching the
    # ones above and below the column headers.
    row_spec(
      nrow(body),
      # #9b9d9e is what the cosmo theme draws around the header row; the
      # generic --bs-border-color is the much fainter between-rows hairline.
      extra_css = "border-bottom: 1px solid #9b9d9e;"
    )
}
