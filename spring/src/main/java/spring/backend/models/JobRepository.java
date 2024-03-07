package spring.backend.models;

import org.springframework.data.jpa.repository.JpaRepository;

public interface JobRepository extends JpaRepository<Job, Integer> {
    // Custom query methods can be added here
}
