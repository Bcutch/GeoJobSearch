import React, {useState, useEffect} from "react";


const DisplayJobs = () => {

  const [jobs, setJobs] = useState([]);

  useEffect (() => {
    fetch("http://localhost:8080/jobs")
      .then(response => response.json())
      .then(data => setJobs(data))
      .catch(error => console.error("Error fetching jobs:", error));
  }, []);

  return (
    <div className="flex justify-center my-4">
      <div className="flex flex-col gap-4">
        {jobs.map((job, index) => (
          <div key={index} className="border p-4 rounded-lg">
            <h2>{job.title}</h2>
            <p>Company: {job.company}</p>
            <p>Location: {job.location}</p>
            <p>Description: {job.description}</p>
            <a href={job.link} target="_blank" rel="noopener noreferrer">
              Apply here
            </a>
            <p>Salary: {job.salary}</p>
            <p>Field: {job.field}</p>
            <p>Remote: {job.is_remote ? 'Yes' : 'No'}</p>
            {/* You can add latitude and longitude if needed */}
          </div>
        ))}
      </div>
    </div>
  );
};

export default DisplayJobs;
