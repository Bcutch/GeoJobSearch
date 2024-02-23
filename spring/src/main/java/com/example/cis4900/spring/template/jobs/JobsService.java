package com.example.cis4900.spring.template.jobs;

import com.example.cis4900.spring.template.jobs.models.Job;

public interface JobsService {

    public String addJob(Job newJob);

    public Job getJob(Integer id);

    public Iterable<Job> allJobs();

    public Integer count();

}
