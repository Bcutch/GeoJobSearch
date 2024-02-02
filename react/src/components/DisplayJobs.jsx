import React from "react";

const exampleJobs = [
  {
    title: "software dev",
    link: "http://www.google.com",
  },
  {
    title: "test2",
    link: "link2",
  },
];

const DisplayJobs = () => {
  return (
    <div className="flex justify-center my-4">
      <div className="flex flex-col gap-4">
        {exampleJobs.map((job, index) => (
          <div key={index} className="border p-4 rounded-lg">
            <h2>{job.title}</h2>
            <a href={job.link} target="_blank" rel="noopener noreferrer">
              Apply here
            </a>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DisplayJobs;
