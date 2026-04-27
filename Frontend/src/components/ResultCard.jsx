const ResultCard = ({ data }) => {
  return (
    <div className="result-card">
  <h3>{data.file}</h3>

  <p>Similarity: {data.similarity}</p>
  <p>Marks: {data.marks}</p>
  <p>Coverage: {data.coverage_score}</p>

  <p><strong>Feedback:</strong> {data.feedback}</p>

  <p><strong>Missing Concepts:</strong></p>
  <ul>
    {data.missing_concepts.map((c, i) => (
      <li key={i}>❌ {c}</li>
    ))}
  </ul>
</div>
  );
};

export default ResultCard;