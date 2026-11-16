ns <- asNamespace("ANCOMBC")
cat("ANCOMBC version:", as.character(packageVersion("ANCOMBC")), "\n")

pattern <- paste(
    "pt\\(",
    "df[[:space:]]*<-",
    "df[[:space:]]*=",
    "p_val.*is.na",
    "p_val.*<-.*1",
    sep="|"
)

shown <- 0L
for (name in ls(ns, all.names=TRUE)) {
    object <- get(name, envir=ns)
    if (!is.function(object)) next
    code <- deparse(body(object), width.cutoff=120)
    hits <- grep(pattern, code)
    if (!length(hits)) next

    cat("\n===== FUNCTION:", name, "=====\n")
    indices <- sort(unique(unlist(lapply(hits, function(i)
        seq.int(max(1L, i-2L), min(length(code), i+3L))))))
    for (i in indices) {
        cat(sprintf("%4d: %s\n", i, code[i]))
        shown <- shown + 1L
        if (shown >= 180L) break
    }
    if (shown >= 180L) {
        cat("\nOutput capped at 180 source lines.\n")
        break
    }
}
