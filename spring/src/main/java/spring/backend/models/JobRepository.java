package spring.backend.models;

import java.util.List;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.jpa.repository.JpaRepository;

public interface JobRepository extends JpaRepository<Job, Integer> {
    // Custom query methods can be added here

    List<Job> findByTitleLike(String title);

    List<Job> findBySalary(Integer salary);

    List<Job> findBySalaryBetween(Integer startSalary, Integer endSalary);

    List<Job>findBySalaryGreaterThan(Integer salary);
    
    //List<Job> findByDistanceBetween(Integer startDistance, Integer endDistance);

    List<Job> findByIsRemoteTrue();

    List<Job> findByIsRemoteFalse();
}
