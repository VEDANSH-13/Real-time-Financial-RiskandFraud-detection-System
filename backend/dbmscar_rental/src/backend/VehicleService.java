package backend;
import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.sql.*;

public class VehicleService {
    public void showVehicles() {
        JFrame frame = new JFrame("🚘 Vehicle Table");
        frame.setSize(700, 400);
        DefaultTableModel model = new DefaultTableModel(
            new String[]{"ID", "Model", "Capacity", "Status", "Rate/km", "Driver ID"}, 0);
        JTable table = new JTable(model);
        frame.add(new JScrollPane(table));

        try (Connection conn = DatabaseConnection.getConnection()) {
            PreparedStatement ps = conn.prepareStatement("SELECT * FROM Vehicle");
            ResultSet rs = ps.executeQuery();
            while (rs.next()) {
                model.addRow(new Object[]{
                    rs.getInt("vehicle_id"), rs.getString("model"), rs.getInt("capacity"),
                    rs.getString("status"), rs.getDouble("rate_per_km"), rs.getInt("driver_id")
                });
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        frame.setVisible(true);
}
}
