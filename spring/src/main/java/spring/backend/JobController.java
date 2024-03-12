package spring.backend.models;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestBody;
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

    @PutMapping("/jobs")
    public List<Job> filterJobs(@RequestBody FilterOptions filterOptions) { //Takes JSON data from request and puts it into filterOptions object
        if (filterOptions.getJobType() != "JobType") {
            if (filterOptions.getJobType() == "Full-time") {
                return jobRepository.findAll();
            }
            if (filterOptions.getJobType() == "Part-time") {
                return jobRepository.findAll();
            }
            if (filterOptions.getJobType() == "Internship") {
                return jobRepository.findAll();
            }
        }
        if (filterOptions.getDistance() != "Distance") {
            if (filterOptions.getDistance() == ">20km") {
                return jobRepository.findAll();
            }
            if (filterOptions.getDistance() == ">50km") {
                return jobRepository.findAll();
            }
            if (filterOptions.getDistance() == ">100km") {
                return jobRepository.findAll();
            }
            if (filterOptions.getDistance() == ">150km") {
                return jobRepository.findAll();
            }
        }
        if (filterOptions.getSalary() != "Salary") {
            if (filterOptions.getSalary() == "$0-$50k") {
                return jobRepository.findBySalaryBetween(0, 50000);
            }
            if (filterOptions.getSalary() == "$50k-$100k") {
                return jobRepository.findBySalaryBetween(50000, 100000);
            }
            if (filterOptions.getSalary() == "$100k-$150k") {
                return jobRepository.findBySalaryBetween(100000, 150000);
            }
            if (filterOptions.getSalary() == "$150k-$200k") {
                return jobRepository.findBySalaryBetween(150000, 200000);
            }
            if (filterOptions.getSalary() == "$200k+") {
                return jobRepository.findBySalaryGreaterThan(200000);
            }
        }

        if (filterOptions.getRemote() != "Remoteness") {
            if (filterOptions.getRemote() == "Remote") {
                return jobRepository.findByIsRemoteTrue();
            }
            if (filterOptions.getRemote() == "Hybrid") {
                return jobRepository.findByIsRemoteTrue();
            }
            if (filterOptions.getRemote() == "On-Site") {
                return jobRepository.findByIsRemoteFalse();
            }
        }

        return jobRepository.findAll();
    }
    
}

