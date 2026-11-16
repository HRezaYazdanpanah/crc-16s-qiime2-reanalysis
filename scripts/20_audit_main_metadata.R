dir.create("reports/main_metadata_audit", recursive=TRUE, showWarnings=FALSE)

m <- read.delim("metadata/main_metadata.tsv", colClasses="character",
                check.names=FALSE, na.strings=c("", "NA", "NaN"))
stopifnot(nrow(m)==80, !anyDuplicated(m[["sample-id"]]))

d <- read.delim("reports/main_braycurtis_14235/distance-matrix.tsv",
                row.names=1, check.names=FALSE)
stopifnot(setequal(rownames(d), m[["sample-id"]]),
          identical(rownames(d), colnames(d)))
m <- m[match(rownames(d), m[["sample-id"]]), ]
stopifnot(identical(m[["sample-id"]], rownames(d)))

for (v in c("dx", "Gender", "Site")) {
    m[[v]] <- trimws(m[[v]])
    m[[v]][!is.na(m[[v]]) & m[[v]]==""] <- NA
    cat("\n", v, "values:\n")
    print(table(m[[v]], useNA="ifany"))
}

for (v in c("Age", "BMI")) {
    raw <- m[[v]]
    x <- suppressWarnings(as.numeric(trimws(raw)))
    bad <- !is.na(raw) & (!is.finite(x) |
           if (v=="BMI") x<=0 else x<0)
    cat("\n", v, "invalid supplied values:\n")
    print(table(raw[bad], useNA="ifany"))
    x[!is.finite(x)] <- NA
    if (v=="BMI") x[x<=0] <- NA else x[x<0] <- NA
    m[[v]] <- x
}
stopifnot(all(m$dx %in% c("normal", "cancer")))

m$dx <- factor(m$dx, levels=c("normal", "cancer"))
m$Gender <- factor(m$Gender)
m$Site <- factor(m$Site)
m$primary_complete <- complete.cases(m[c("dx","Age","Gender","BMI","Site")])
m$noBMI_complete <- complete.cases(m[c("dx","Age","Gender","Site")])
m$missing_fields <- apply(is.na(m[c("dx","Age","Gender","BMI","Site")]), 1,
                         function(x) paste(names(x)[x], collapse=";"))

cat("\nBMI missing/invalid percent: overall\n")
print(100*mean(is.na(m$BMI)))
cat("\nBMI missing/invalid percent: by dx\n")
print(100*tapply(is.na(m$BMI), m$dx, mean))

for (label in c("all", "primary_complete", "noBMI_complete")) {
    s <- if (label=="all") m else m[m[[label]], ]
    cat("\nSAMPLE SET:", label, "n=", nrow(s), "\n")
    print(table(s$dx, s$Site))
}

cc <- droplevels(m[m$primary_complete, ])
cat("\nPRIMARY MODEL DESIGN CHECK\n")
if (nrow(cc)>0 && all(sapply(cc[c("dx","Gender","Site")], nlevels)>=2)) {
    X <- model.matrix(~ dx + Age + Gender + BMI + Site, data=cc)
    cat("Columns:", ncol(X), "Rank:", qr(X)$rank,
        "Residual df:", nrow(X)-qr(X)$rank, "\n")
} else {
    cat("STOP FOR REVIEW: insufficient cases or factor levels.\n")
}

write.table(m, "reports/main_metadata_audit/audited_metadata.tsv",
            sep="\t", quote=FALSE, row.names=FALSE, na="")
cat("\nCOMPLETE: metadata audit only; no association tests fitted.\n")
