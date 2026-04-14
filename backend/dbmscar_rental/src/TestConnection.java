import java.sql.*;

public class TestConnection {
    public static void main(String[] args) {
        try {
            Connection conn = DriverManager.getConnection(
                "jdbc:mysql://localhost:3306/car_rental",
                "root",     // change if needed
                "your_password" // change to your password
            );
            Statement st = conn.createStatement();
            ResultSet rs = st.executeQuery("SELECT COUNT(*) FROM Driver");
            if (rs.next()) {
                System.out.println("✅ Connected! Driver count = " + rs.getInt(1));
            }
            conn.close();
        } catch (SQLException e) {
            e.printStackTrace();
}
}
}