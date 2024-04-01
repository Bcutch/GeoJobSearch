import React, { useState, useEffect } from "react";

const DisplayJobs = (prop) => {

  useEffect(() => {
    fetch("/api/jobs")
      .then((response) => response.json())
      .then((data) => {prop.setJobs(data)})
      .catch((error) => console.error("Error fetching jobs:", error));
  }, []);
  
  const [selectedJob, setSelectedJob] = useState(prop.jobs[1])
  const handleClick = (jobId) => {
        const selected = prop.jobs.find(job => job.id == jobId)
        setSelectedJob(selected)
    }

  return (
    <div className="flex justify-center bg-gray-100">
      <div className="flex flex-col gap-4 w-1/2 m-3 p-3 max-h-[75vh] overflow-y-auto">
        {prop.jobs.map((job, index) => (
          <div key={index} className="border p-4 rounded-lg bg-white" onClick={() => handleClick(job.id)}>
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
          <div className="flex flex-col w-[40%] h-[60vh] m-3 border p-4 rounded-lg overflow-y-auto bg-white">
            <h3>{selectedJob.title}</h3>
              <p><strong>Location:</strong> {selectedJob.location}</p>
              <p><strong>Salary:</strong> {selectedJob.salary}</p>
              <p><strong>Job Description: </strong>{selectedJob.description}</p>
              <div className="flex items-end w-full h-full justify-center">
                <button className="btn btn-primary align-bottom"><a href={selectedJob.url} target="_blank" rel="noreferrer" className="text-white">Apply Here</a></  button>
              </div>
          </div>
        ) : (
          <p>Select a job to see details</p>
        )}
    </div>
  );
};

export default DisplayJobs;
