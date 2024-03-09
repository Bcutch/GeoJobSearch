import React, { useState, useEffect } from "react";

const DisplayJobs = () => {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8080/jobs")
      .then((response) => response.json())
      .then((data) => setJobs(data))
      .catch((error) => console.error("Error fetching jobs:", error));
  }, []);
  
  const [selectedJob, setSelectedJob] = useState(jobs[1])
  const handleClick = (jobId) => {
        const selected = jobs.find(job => job.id == jobId)
        setSelectedJob(selected)
    }

  return (
    <div className="flex justify-center my-4">
      <div className="flex flex-col gap-4 w-1/2 m-3">
        {jobs.map((job, index) => (
          <div key={index} className="border p-4 rounded-lg" onClick={() => handleClick(job.id)}>
            <h2>{job.title}</h2>
            <p>Location: {job.location}</p>
            <a href={job.url} target="_blank" rel="noopener noreferrer">
              Apply here
            </a>
            <p>Salary: {job.salary}</p>
            {/* You can add latitude and longitude if needed */}
          </div>
        ))}
      </div>
      {selectedJob ? (
          <div className="flex flex-col w-[40%] h-[60vh] m-3 border p-4 rounded-lg overflow-y-auto">
            <h3>{selectedJob.title}</h3>
              <p><strong>Location:</strong> {selectedJob.location}</p>
              <p><strong>Salary:</strong> {selectedJob.salary}</p>
              <p><strong>Job Description: </strong>{selectedJob.description}</p>
              <div className="flex items-end w-full h-full justify-center">
                <button className="btn btn-primary align-bottom"><a href={selectedJob.url} target="_blank" className="text-white">Apply Here</a></  button>
              </div>
          </div>
        ) : (
          <p>Select a job to see details</p>
        )}
    </div>
  );
};

export default DisplayJobs;
