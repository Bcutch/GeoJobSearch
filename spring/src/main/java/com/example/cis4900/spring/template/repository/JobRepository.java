package com.example.cis4900.spring.template.repository;

import com.example.cis4900.spring.template.Job;
import org.springframework.data.jpa.repository.JpaRepository;

public interface JobRepository extends JpaRepository<Job, Long> {
}
