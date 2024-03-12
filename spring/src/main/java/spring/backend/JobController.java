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
        if (!filterOptions.getJobType().equals("Job Type")) {
            if (filterOptions.getJobType().equals("Full-time")) {
                return jobRepository.findAll();
            }
            if (filterOptions.getJobType().equals("Part-time")) {
                return jobRepository.findAll();
            }
            if (filterOptions.getJobType().equals("Internship")) {
                return jobRepository.findAll();
            }
        }
        if (!filterOptions.getDistance().equals("Distance")) {
            if (filterOptions.getDistance().equals(">20km")) {
                return jobRepository.findAll();
            }
            if (filterOptions.getDistance().equals(">50km")) {
                return jobRepository.findAll();
            }
            if (filterOptions.getDistance().equals(">100km")) {
                return jobRepository.findAll();
            }
            if (filterOptions.getDistance().equals(">150km")) {
                return jobRepository.findAll();
            }
        }
        if (!filterOptions.getSalary().equals("Salary")) {
            if (filterOptions.getSalary().equals("$0-$50k")) {
                return jobRepository.findBySalaryBetween(0, 50000);
            }
            if (filterOptions.getSalary().equals("$50k-$100k")) {
                return jobRepository.findBySalaryBetween(50000, 100000);
            }
            if (filterOptions.getSalary().equals("$100k-$150k")) {
                return jobRepository.findBySalaryBetween(100000, 150000);
            }
            if (filterOptions.getSalary().equals("$150k-$200k")) {
                return jobRepository.findBySalaryBetween(150000, 200000);
            }
            if (filterOptions.getSalary().equals("$200k+")) {
                return jobRepository.findBySalaryGreaterThan(200000);
            }
        }

        if (!filterOptions.getRemote().equals("Remoteness")) {
            if (filterOptions.getRemote().equals("Remote")) {
                return jobRepository.findByIsRemoteTrue();
            }
            if (filterOptions.getRemote().equals("Hybrid")) {
                return jobRepository.findByIsRemoteTrue();
            }
            if (filterOptions.getRemote().equals("On-Site")) {
                return jobRepository.findByIsRemoteFalse();
            }
        }

        return jobRepository.findAll();
    }
    
}

