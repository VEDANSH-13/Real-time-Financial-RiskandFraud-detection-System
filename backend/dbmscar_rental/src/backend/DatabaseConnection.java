package backend;
import java.sql.*;

public class DatabaseConnection {
    private static final String URL = "jdbc:mysql://localhost:3306/car_rental1";
    private static final String USER = "root";
    private static final String PASS = "Vedansh13@"; 

    public static Connection getConnection() throws SQLException {
        return DriverManager.getConnection(URL, USER,PASS);
}
}