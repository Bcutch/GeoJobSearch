package spring.backend;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.annotation.DirtiesContext;
import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@DirtiesContext // Use this if you want to reset the Spring ApplicationContext after this test class
public class TestDatabase {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Test
    void testConnection() {
        //will display the db it is connected to along with the version number to make sure the dpring is connected to a database
        // expected output = mariaDB{version_number}
        // This query is almost universally supported and doesn't depend on your schema
        String version = jdbcTemplate.queryForObject("SELECT VERSION();", String.class);
        assertThat(version).isNotNull();
        System.out.println("Database Version: " + version);
    }
}

