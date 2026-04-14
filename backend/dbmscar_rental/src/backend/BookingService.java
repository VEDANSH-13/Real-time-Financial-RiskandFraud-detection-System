package backend;
import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.sql.*;

public class BookingService {

    public double createBooking(String name, String phone, String address, int vehicleId, double distance) throws SQLException {
        try (Connection conn = DatabaseConnection.getConnection()) {
            // Insert user
            PreparedStatement userPs = conn.prepareStatement(
                "INSERT INTO User(name, phone, address) VALUES (?, ?, ?)",
                Statement.RETURN_GENERATED_KEYS
            );
            userPs.setString(1, name);
            userPs.setString(2, phone);
            userPs.setString(3, address);
            userPs.executeUpdate();
            ResultSet userRs = userPs.getGeneratedKeys();
            userRs.next();
            int userId = userRs.getInt(1);

            // Get rate per km
            PreparedStatement vPs = conn.prepareStatement("SELECT rate_per_km FROM Vehicle WHERE vehicle_id=?");
            vPs.setInt(1, vehicleId);
            ResultSet vRs = vPs.executeQuery();
            vRs.next();
            double rate = vRs.getDouble("rate_per_km");
            double total = rate * distance;

            // Insert booking
            PreparedStatement bookPs = conn.prepareStatement(
                "INSERT INTO Booking(user_id, vehicle_id, booking_date, distance_km, total_amount, status) VALUES (?, ?, CURDATE(), ?, ?, 'confirmed')");
            bookPs.setInt(1, userId);
            bookPs.setInt(2, vehicleId);
            bookPs.setDouble(3, distance);
            bookPs.setDouble(4, total);
            bookPs.executeUpdate();

            return total;
        }
    }

    public void showBookings() {
        JFrame frame = new JFrame("📋 All Bookings");
        frame.setSize(700, 400);
        DefaultTableModel model = new DefaultTableModel(new String[]{"ID", "Customer", "Vehicle", "Date", "Km", "Amount", "Status"}, 0);
        JTable table = new JTable(model);
        frame.add(new JScrollPane(table));

        try (Connection conn = DatabaseConnection.getConnection()) {
            PreparedStatement ps = conn.prepareStatement(
                "SELECT b.booking_id, u.name, v.model, b.booking_date, b.distance_km, b.total_amount, b.status " +
                "FROM Booking b JOIN User u ON b.user_id=u.user_id JOIN Vehicle v ON b.vehicle_id=v.vehicle_id");
            ResultSet rs = ps.executeQuery();
            while (rs.next()) {
                model.addRow(new Object[]{
                    rs.getInt(1), rs.getString(2), rs.getString(3),
                    rs.getString(4), rs.getDouble(5), rs.getDouble(6), rs.getString(7)
                });
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        frame.setVisible(true);
}
}