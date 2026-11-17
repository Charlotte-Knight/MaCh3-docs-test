var Scorer = {
  score: ([docname, , anchor, , score, , kind]) => {
    const pythonApi = docname.startsWith("pymach3/") && (
      kind === "object" || anchor.startsWith("#pyMaCh3.") ||
      anchor.startsWith("#module-pyMaCh3.") || anchor === "#api-reference"
    );
    return docname.startsWith("api/") || pythonApi ? score - 20 : score;
  },
  objNameMatch: 11,
  objPartialMatch: 6,
  objPrio: { 0: 15, 1: 5, 2: -5 },
  objPrioDefault: 0,
  title: 15,
  partialTitle: 7,
  term: 5,
  partialTerm: 2,
};
