package com.example.cis4900.spring.template.jobs.dao;

import com.example.cis4900.spring.template.jobs.models.Job;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;


public interface JobsDao extends CrudRepository<Job, Integer> {

    @Query("SELECT COUNT(*) FROM Job")
    Integer getCount();

    
}
