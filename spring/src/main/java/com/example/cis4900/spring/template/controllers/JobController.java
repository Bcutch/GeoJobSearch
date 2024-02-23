package com.example.cis4900.spring.template.controllers;

import com.example.cis4900.spring.template.jobs.models.Job;
import com.example.cis4900.spring.template.jobs.JobsService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping(path = "/api/jobs")
public class JobController {

    private JobsService jobsService;

    @Autowired
    JobController(JobsService jobsService){
        this.jobsService = jobsService;
    }

    @PostMapping("/add")
    private @ResponseBody String addJob(@RequestBody Job newJob){
        return jobsService.addJob(newJob);
    }

    @GetMapping("/get/{id}")
    private @ResponseBody Job getJob(@PathVariable Integer id){
        return jobsService.getJob(id);
    }

    @GetMapping("/all")
    private @ResponseBody Iterable<Job> allJobs() {
        return jobsService.allJobs();
    }

    @GetMapping("/count")
    private @ResponseBody Integer count() {
        return jobsService.count();
    }


}




