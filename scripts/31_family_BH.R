d <- read.delim(
    "reports/main_ancombc2/dx_cancer_audited_unadjusted.tsv",
    check.names=FALSE, stringsAsFactors=FALSE,
    na.strings=c("", "NA", "NaN"))
stopifnot(nrow(d)==194, !anyDuplicated(d$taxonomy))
valid <- tolower(as.character(d$valid_estimate)) == "true"
stopifnot(sum(valid)==193,
          sum(d$family=="confirmatory")==4,
          sum(d$family=="exploratory")==190,
          all(d$genus_label[!valid]=="S5-A14a"),
          all(d$family[!valid]=="exploratory"))

names(d)[names(d)=="q"] <- "q_exported_unadjusted"
d$q_family_BH <- NA_real_

for (family in c("confirmatory", "exploratory")) {
    n_family <- if (family=="confirmatory") 5L else 190L
    keep <- which(d$family==family & valid)
    d$q_family_BH[keep] <- p.adjust(
        d$p[keep], method="BH", n=n_family)
}

d$reject_family_BH <- NA
d$reject_family_BH[valid] <- d$q_family_BH[valid] < 0.05
d$direction <- NA_character_
d$direction[valid] <- ifelse(
    d$lfc[valid] > 0, "higher_in_cancer",
    ifelse(d$lfc[valid] < 0, "lower_in_cancer", "zero"))
d$status <- ifelse(valid, "numerically_evaluable",
                   "not_evaluable_missing_estimate")

write.table(d, "reports/main_ancombc2/dx_cancer_family_BH.tsv",
            sep="\t", quote=FALSE, row.names=FALSE, na="")

targets <- c("Fusobacterium", "Parvimonas", "Peptostreptococcus",
             "Porphyromonas", "Solobacterium")
confirmatory <- d[match(targets, d$genus_label), ]
confirmatory$genus_label <- targets
confirmatory$status[targets=="Solobacterium"] <-
    "not_evaluable_prevalence_7_of_80"

cols <- c("genus_label", "lfc", "se", "p", "q_family_BH",
          "passed_ss", "direction", "status")
write.table(confirmatory[, cols],
            "reports/main_ancombc2/confirmatory_five_BH.tsv",
            sep="\t", quote=FALSE, row.names=FALSE, na="")

cat("\nCONFIRMATORY HYPOTHESES — BH family n=5\n")
print(confirmatory[, cols], row.names=FALSE, digits=5)

cat("\nBH REJECTIONS BY FAMILY\n")
for (family in c("confirmatory", "exploratory")) {
    rows <- d$family==family
    cat(family, ":",
        sum(d$reject_family_BH[rows], na.rm=TRUE), "\n")
}

cat("\nEXPLORATORY: first 10 by family-adjusted p-value\n")
e <- d[d$family=="exploratory" & valid, ]
e <- e[order(e$q_family_BH, e$p), ]
print(head(e[, cols], 10), row.names=FALSE, digits=5)
cat("\nCOMPLETE: separate BH adjustments; no model refitted.\n")
