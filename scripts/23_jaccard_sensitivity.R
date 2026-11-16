library(vegan)

out <- "reports/main_primary"
stopifnot(!file.exists(file.path(out, "jaccard_adonis2.tsv")))
saved <- readRDS(file.path(out, "permutations_within_site.rds"))

m <- read.delim("reports/main_metadata_audit/audited_metadata.tsv",
                colClasses="character", check.names=FALSE,
                na.strings=c("", "NA"))
stopifnot(!anyDuplicated(m[["sample-id"]]),
          setequal(m[["sample-id"]], saved$sample_ids))
m <- m[match(saved$sample_ids, m[["sample-id"]]), ]
stopifnot(identical(m[["sample-id"]], saved$sample_ids))

m$Age <- as.numeric(m$Age)
m$BMI <- as.numeric(m$BMI)
m$dx <- factor(m$dx, levels=c("normal", "cancer"))
m$Gender <- factor(m$Gender)
m$Site <- factor(m$Site)
stopifnot(nrow(m)==80,
          all(complete.cases(m[c("dx","Age","Gender","BMI","Site")])))

D <- as.matrix(read.delim(
    "reports/main_jaccard_14235/distance-matrix.tsv",
    row.names=1, check.names=FALSE))
storage.mode(D) <- "double"
stopifnot(identical(rownames(D), colnames(D)),
          setequal(rownames(D), saved$sample_ids))
D <- D[saved$sample_ids, saved$sample_ids]
stopifnot(all(is.finite(D)), all(D >= 0), all(D <= 1),
          max(abs(D-t(D))) < 1e-10,
          max(abs(diag(D))) < 1e-10,
          nrow(saved$indices)==9999,
          all(apply(saved$indices, 1, function(p)
              all(m$Site[p] == m$Site))))

distance <- as.dist(D)
fit <- adonis2(
    distance ~ dx + Age + Gender + BMI + Site,
    data=m, permutations=saved$indices, by="margin",
    sqrt.dist=FALSE, add=FALSE, parallel=1,
    na.action=na.fail
)

result <- data.frame(term=rownames(fit), as.data.frame(fit),
                     row.names=NULL, check.names=FALSE)
write.table(result, file.path(out, "jaccard_adonis2.tsv"),
            sep="\t", quote=FALSE, row.names=FALSE)
saveRDS(fit, file.path(out, "jaccard_adonis2.rds"))
capture.output(sessionInfo(),
               file=file.path(out, "jaccard_sessionInfo.txt"))
print(fit)
cat("\nCOMPLETE: planned Jaccard sensitivity; primary unchanged.\n")
