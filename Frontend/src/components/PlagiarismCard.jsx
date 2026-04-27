const PlagiarismCard = ({ caseData }) => {
  if (!caseData) return null;

  return (
    <div className="plag-card">
  <h3>{caseData.message}</h3>

  <p>Similarity: {caseData.similarity}</p>

  <p><strong>Copied Parts:</strong></p>
  <ul>
    {caseData.copied_parts.map((line, i) => (
      <li key={i}>"{line}"</li>
    ))}
  </ul>
</div>
  );
};

export default PlagiarismCard;
