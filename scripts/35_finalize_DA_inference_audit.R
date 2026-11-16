root <- "reports/main_ancombc2"
d <- read.delim(file.path(root, "dx_cancer_family_BH.tsv"),
                check.names=FALSE, na.strings=c("", "NA", "NaN"))
a <- read.delim(file.path(root, "nonzero_support_audit.tsv"),
                check.names=FALSE, na.strings=c("", "NA", "NaN"))

stopifnot(!anyDuplicated(a$taxonomy),
          setequal(d$taxonomy, a$taxonomy))
a <- a[match(d$taxonomy, a$taxonomy), ]
d$nonzero_residual_df <- a$nonzero_residual_df
numeric_ok <- tolower(as.character(d$valid_estimate)) == "true"
ok <- numeric_ok & d$nonzero_residual_df > 0
stopifnot(sum(ok)==188, sum(d$nonzero_residual_df<=0)==5)

d$q_family_BH_before_support_audit <- d$q_family_BH
d$q_family_BH <- NA_real_
for (family in c("confirmatory", "exploratory")) {
    keep <- which(ok & d$family==family)
    n <- if (family=="confirmatory") 5L else 190L
    d$q_family_BH[keep] <- p.adjust(d$p[keep], method="BH", n=n)
}
stopifnot(isTRUE(all.equal(
    d$q_family_BH[ok],
    d$q_family_BH_before_support_audit[ok],
    tolerance=1e-12)))

d$inference_evaluable <- ok
d$status <- ifelse(
    !numeric_ok, "not_evaluable_missing_estimate",
    ifelse(d$nonzero_residual_df<=0,
           "not_evaluable_zero_nonzero_support_df",
           "evaluable_after_support_audit"))
d$reject_family_BH <- NA
d$reject_family_BH[ok] <- d$q_family_BH[ok] < 0.05
d$p_exported <- d$p
d$p[!ok] <- NA_real_
d$direction[!ok] <- NA_character_

write.table(d, file.path(root, "dx_cancer_final_audited.tsv"),
            sep="\t", quote=FALSE, row.names=FALSE, na="")

cat("Inference-evaluable groups:", sum(ok), "\n")
cat("BH values for evaluable groups unchanged: PASS\n")
cat("\nNon-evaluable groups:\n")
print(d[!ok, c("genus_label", "status")], row.names=FALSE)
cat("\nFinal BH findings:\n")
print(d[which(d$reject_family_BH),
        c("genus_label","family","lfc","se","q_family_BH","passed_ss")],
      row.names=FALSE)
