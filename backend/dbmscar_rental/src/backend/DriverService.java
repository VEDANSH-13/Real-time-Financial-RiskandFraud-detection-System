package backend;
import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.sql.*;

public class DriverService {
    public void showDrivers() {
        JFrame frame = new JFrame("👨‍✈ Driver Table");
        frame.setSize(600, 400);
        DefaultTableModel model = new DefaultTableModel(
            new String[]{"Driver ID", "Name", "Phone", "Status"}, 0);
        JTable table = new JTable(model);
        frame.add(new JScrollPane(table));

        try (Connection conn = DatabaseConnection.getConnection()) {
            PreparedStatement ps = conn.prepareStatement("SELECT * FROM Driver");
            ResultSet rs = ps.executeQuery();
            while (rs.next()) {
                model.addRow(new Object[]{
                    rs.getInt("driver_id"), rs.getString("name"),
                    rs.getString("phone"), rs.getString("status")
                });
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        frame.setVisible(true);
}
}
