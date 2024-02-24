package spring.backend;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.CrossOrigin;


@RestController
public class HelloController {

    @GetMapping("/jobs")
    @CrossOrigin(origins = "http://localhost:3000") // Allow requests from this origin

    public String getJobs() {
        return "Here are jobs!";
    }
}
