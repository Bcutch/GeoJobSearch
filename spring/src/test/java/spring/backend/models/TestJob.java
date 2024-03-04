package spring.backend.models;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import spring.backend.models.Job;

public class TestJob {

    @Test
    void testGetterAndSetter() {

        Job job = new Job();

        job.setTitle("Software Engineer");
        job.setCompany("Example Inc.");
        job.setLocation("New York");
        job.setDescription("This is a job description");
        job.setUrl("https://example.com/job");
        job.setSalary(80000);
        job.setField("Technology");
        job.setIsRemote(true);
        job.setLatitude(40.7128);
        job.setLongitude(-74.0060);


        assertEquals("Software Engineer", job.getTitle());
        assertEquals("Example Inc.", job.getCompany());
        assertEquals("New York", job.getLocation());
        assertEquals("This is a job description", job.getDescription());
        assertEquals("https://example.com/job", job.getUrl());
        assertEquals(80000, job.getSalary());
        assertEquals("Technology", job.getField());
        assertTrue(job.getIsRemote());
        assertEquals(40.7128, job.getLatitude());
        assertEquals(-74.0060, job.getLongitude());

    }

}
