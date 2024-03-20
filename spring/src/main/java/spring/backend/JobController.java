package spring.backend.models;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RestController;

import spring.backend.models.FilterOptions;
import spring.backend.models.Job;
import spring.backend.models.JobRepository;

import org.springframework.web.bind.annotation.RequestBody;

import java.util.ArrayList;
import java.util.List;
import java.io.*;

@RestController
public class JobController {

    private final JobRepository jobRepository;

    @Autowired
    public JobController(JobRepository jobRepository) {
        this.jobRepository = jobRepository;
    }

    @GetMapping("/jobs")
    public List<Job> getAllJobs() {
        return jobRepository.findAll();
    }

    private List<Job> combineResults(List<Job> first, List<Job> second) {
        List<Job> ret = new ArrayList<>();

        for (Job job : first) {
            for (Job jobComp : second) {
                if (job.getId() == jobComp.getId()) {
                    ret.add(job);
                    break;
                }
            }
        }

        return ret;
    }

    @PutMapping("/jobs")
    public List<Job> filterJobs(@RequestBody FilterOptions filterOptions) { //Takes JSON data from request and puts it into filterOptions object
        List<Job> jobTypeList = new ArrayList<>();
        List<Job> distanceList = new ArrayList<>();
        List<Job> salaryList = new ArrayList<>();
        List<Job> remoteList = new ArrayList<>();
        
        if (!filterOptions.getJobType().equals("Job Type")) {
            if (filterOptions.getJobType().equals("Full-time")) {
                jobTypeList.addAll(jobRepository.findAll());
            }
            if (filterOptions.getJobType().equals("Part-time")) {
                jobTypeList.addAll(jobRepository.findAll());
            }
            if (filterOptions.getJobType().equals("Internship")) {
                jobTypeList.addAll(jobRepository.findAll());
            }
        } else {
            jobTypeList.addAll(jobRepository.findAll());
        }

        if (!filterOptions.getDistance().equals("Distance")) {
            if (filterOptions.getDistance().equals(">20km")) {
                distanceList.addAll(jobRepository.findAll());
            }
            if (filterOptions.getDistance().equals(">50km")) {
                distanceList.addAll(jobRepository.findAll());
            }
            if (filterOptions.getDistance().equals(">100km")) {
                distanceList.addAll(jobRepository.findAll());
            }
            if (filterOptions.getDistance().equals(">150km")) {
                distanceList.addAll(jobRepository.findAll());
            }
        } else {
            distanceList.addAll(jobRepository.findAll());
        }

        if (!filterOptions.getSalary().equals("Salary")) {
            if (filterOptions.getSalary().equals("$0-$50k")) {
                salaryList.addAll(jobRepository.findBySalaryBetween(0, 50000));
            }
            if (filterOptions.getSalary().equals("$50k-$100k")) {
                salaryList.addAll(jobRepository.findBySalaryBetween(50000, 100000));
            }
            if (filterOptions.getSalary().equals("$100k-$150k")) {
                salaryList.addAll(jobRepository.findBySalaryBetween(100000, 150000));
            }
            if (filterOptions.getSalary().equals("$150k-$200k")) {
                salaryList.addAll(jobRepository.findBySalaryBetween(150000, 200000));
            }
            if (filterOptions.getSalary().equals("$200k+")) {
                salaryList.addAll(jobRepository.findBySalaryGreaterThan(200000));
            }
        } else {
            salaryList.addAll(jobRepository.findAll());
        }

        if (!filterOptions.getRemote().equals("Remoteness")) {
            if (filterOptions.getRemote().equals("Remote")) {
                remoteList.addAll(jobRepository.findByIsRemoteTrue());
            }
            if (filterOptions.getRemote().equals("Hybrid")) {
                remoteList.addAll(jobRepository.findByIsRemoteTrue());
            }
            if (filterOptions.getRemote().equals("On-Site")) {
                remoteList.addAll(jobRepository.findByIsRemoteFalse());
            }
        } else {
            remoteList.addAll(jobRepository.findAll());
        }

        List<Job> firstCombine = combineResults(salaryList, remoteList);
        List<Job> secondCombine = combineResults(distanceList, jobTypeList);
        return combineResults(firstCombine, secondCombine);
    }
    
}

