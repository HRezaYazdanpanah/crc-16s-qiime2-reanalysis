library(vegan)
library(permute)

out <- "reports/main_primary"
dir.create(out, recursive=TRUE, showWarnings=FALSE)
stopifnot(!file.exists(file.path(out, "braycurtis_adonis2.tsv")))

m <- read.delim("reports/main_metadata_audit/audited_metadata.tsv",
                colClasses="character", check.names=FALSE,
                na.strings=c("", "NA"))
D <- as.matrix(read.delim(
    "reports/main_braycurtis_14235/distance-matrix.tsv",
    row.names=1, check.names=FALSE))
storage.mode(D) <- "double"

stopifnot(!anyDuplicated(m[["sample-id"]]),
          identical(rownames(D), colnames(D)),
          setequal(rownames(D), m[["sample-id"]]),
          all(is.finite(D)), all(D >= 0),
          max(abs(D-t(D))) < 1e-10,
          max(abs(diag(D))) < 1e-10)

m <- m[match(rownames(D), m[["sample-id"]]), ]
m$Age <- as.numeric(m$Age)
m$BMI <- as.numeric(m$BMI)
m$dx <- factor(m$dx, levels=c("normal", "cancer"))
m$Gender <- factor(m$Gender)
m$Site <- factor(m$Site)

stopifnot(nrow(m)==80,
          all(complete.cases(m[c("dx","Age","Gender","BMI","Site")])))
X <- model.matrix(~ dx + Age + Gender + BMI + Site, data=m)
stopifnot(qr(X)$rank == ncol(X), nrow(X) > ncol(X))

set.seed(20261011)
control <- how(nperm=9999, blocks=m$Site)
P <- shuffleSet(nrow(m), nset=9999, control=control)

stopifnot(all(apply(P, 1, function(p)
    all(as.character(m$Site[p]) == as.character(m$Site)))))

saveRDS(list(indices=P, sample_ids=m[["sample-id"]],
             seed=20261011, control=control),
        file.path(out, "permutations_within_site.rds"))

cat("Samples:", nrow(m), "\n")
cat("Requested permutations: 9999\n")
cat("Generated permutations:", nrow(P), "\n")
cat("Unique generated permutations:", nrow(unique(P)), "\n")
cat("All permutations restricted within Site: PASS\n")

distance <- as.dist(D)
fit <- adonis2(
    distance ~ dx + Age + Gender + BMI + Site,
    data=m, permutations=P, by="margin",
    sqrt.dist=FALSE, add=FALSE, parallel=1,
    na.action=na.fail
)

result <- data.frame(term=rownames(fit), as.data.frame(fit),
                     row.names=NULL, check.names=FALSE)
write.table(result, file.path(out, "braycurtis_adonis2.tsv"),
            sep="\t", quote=FALSE, row.names=FALSE)
saveRDS(fit, file.path(out, "braycurtis_adonis2.rds"))
writeLines(m[["sample-id"]], file.path(out, "primary_sample_ids.txt"))
capture.output(sessionInfo(), file=file.path(out, "sessionInfo.txt"))

print(fit)
cat("\nCOMPLETE: primary Bray-Curtis marginal PERMANOVA.\n")
