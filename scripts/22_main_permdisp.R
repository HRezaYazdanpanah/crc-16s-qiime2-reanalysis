library(vegan)

out <- "reports/main_primary"
stopifnot(!file.exists(file.path(out, "braycurtis_permdisp.tsv")))
saved <- readRDS(file.path(out, "permutations_within_site.rds"))

m <- read.delim("reports/main_metadata_audit/audited_metadata.tsv",
                colClasses="character", check.names=FALSE)
m <- m[match(saved$sample_ids, m[["sample-id"]]), ]
stopifnot(identical(m[["sample-id"]], saved$sample_ids))
group <- factor(m$dx, levels=c("normal", "cancer"))

D <- as.matrix(read.delim(
    "reports/main_braycurtis_14235/distance-matrix.tsv",
    row.names=1, check.names=FALSE))
D <- D[saved$sample_ids, saved$sample_ids]
stopifnot(all(apply(saved$indices, 1, function(p)
    all(m$Site[p] == m$Site))))

bd <- betadisper(as.dist(D), group, type="median",
                 bias.adjust=FALSE, sqrt.dist=FALSE, add=FALSE)
test <- permutest(bd, permutations=saved$indices,
                 pairwise=FALSE, parallel=1)

write.table(
    data.frame(term=rownames(test$tab), test$tab, row.names=NULL),
    file.path(out, "braycurtis_permdisp.tsv"),
    sep="\t", quote=FALSE, row.names=FALSE)
write.table(
    data.frame("sample-id"=saved$sample_ids, dx=group,
               distance_to_median=bd$distances, check.names=FALSE),
    file.path(out, "braycurtis_dispersion_distances.tsv"),
    sep="\t", quote=FALSE, row.names=FALSE)
saveRDS(list(model=bd, test=test),
        file.path(out, "braycurtis_permdisp.rds"))

cat("Positive eigenvalues:", sum(bd$eig > 0), "\n")
cat("Negative eigenvalues:", sum(bd$eig < 0), "\n")
cat("\nMean distance to group spatial median:\n")
print(tapply(bd$distances, group, mean))
print(test)
cat("\nCOMPLETE: planned Bray-Curtis PERMDISP.\n")
