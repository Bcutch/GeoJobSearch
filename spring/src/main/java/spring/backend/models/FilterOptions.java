package spring.backend.models;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table
public class FilterOptions {
    private @Id @GeneratedValue(strategy = GenerationType.IDENTITY) Long id;

    private String jobType = "Job Type";
    private String remote = "Remoteness";
    private String salary = "Salary";
    private String distance = "Distance";

    public FilterOptions() {
        
    }

    public FilterOptions(String jobTypes, String remotes, String salarys, String distances) {
        jobType = jobTypes;
        remote = remotes;
        salary = salarys;
        distance = distances;
    }

    // Getters
    public String getJobType() {
        return jobType;
    }

    public String getDistance() {
        return distance;
    }

    public String getSalary() {
        return salary;
    }

    public String getRemote() {
        return remote;
    }

    // Setters
    public void setJobType(String jobType) {
        this.jobType = jobType;
    }

    public void setDistance(String distance) {
        this.distance = distance;
    }

    public void setSalary(String salary) {
        this.salary = salary;
    }

    public void setRemote(String remote) {
        this.remote = remote;
    }

}
