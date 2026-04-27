import React, { useState } from "react";
import UploadBox from "../components/UploadBox";
import ResultCard from "../components/ResultCard";
import PlagiarismCard from "../components/PlagiarismCard";
import Charts from "../components/Charts";

const Dashboard = () => {
  const [result, setResult] = useState(null);

  return (
    <div className="p-6">
      <UploadBox setResult={setResult} />

      {result && (
        <>
          <Charts data={result.evaluations} />

          <h2 className="mt-6 font-bold text-xl">Results</h2>
          {result.evaluations.map((res, i) => (
            <ResultCard key={i} data={res} />
          ))}

          <h2 className="mt-6 font-bold text-xl text-red-600">
            Plagiarism Cases
          </h2>
          {result.plagiarism_cases.map((p, i) => (
            <PlagiarismCard key={i} caseData={p} />
          ))}
        </>
      )}
    </div>
  );
};

export default Dashboard;