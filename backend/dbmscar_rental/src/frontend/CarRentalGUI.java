package frontend;

import backend.*;
import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.*;
import java.sql.*;

public class CarRentalGUI extends JFrame {

    private JTextField nameField, phoneField, addressField, distanceField;
    private JComboBox<String> vehicleBox;

    private BookingService bookingService;
    private VehicleService vehicleService;
    private DriverService driverService;

    public CarRentalGUI() {
        // Initialize backend services
        bookingService = new BookingService();
        vehicleService = new VehicleService();
        driverService = new DriverService();

        setTitle("🚗 Car Rental System");
        setSize(750, 550);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        JLabel title = new JLabel("Car Rental Booking System", JLabel.CENTER);
        title.setFont(new Font("Arial", Font.BOLD, 22));
        add(title, BorderLayout.NORTH);

        JPanel panel = new JPanel(new GridLayout(8, 2, 10, 10));
        panel.setBorder(BorderFactory.createEmptyBorder(20, 40, 20, 40));

        panel.add(new JLabel("Customer Name:"));
        nameField = new JTextField();
        panel.add(nameField);

        panel.add(new JLabel("Phone:"));
        phoneField = new JTextField();
        panel.add(phoneField);

        panel.add(new JLabel("Address:"));
        addressField = new JTextField();
        panel.add(addressField);

        panel.add(new JLabel("Select Vehicle:"));
        vehicleBox = new JComboBox<>();
        loadVehicles();
        panel.add(vehicleBox);

        panel.add(new JLabel("Distance (km):"));
        distanceField = new JTextField();
        panel.add(distanceField);

        JButton bookBtn = new JButton("Book Vehicle");
        JButton viewBookingBtn = new JButton("View All Bookings");
        JButton viewVehicleBtn = new JButton("View Vehicles");
        JButton viewDriverBtn = new JButton("View Drivers");
        JButton exitBtn = new JButton("Exit");

        panel.add(bookBtn);
        panel.add(viewBookingBtn);
        panel.add(viewVehicleBtn);
        panel.add(viewDriverBtn);
        panel.add(exitBtn);

        add(panel, BorderLayout.CENTER);

        // Action Listeners
        bookBtn.addActionListener(e-> bookVehicle());
        viewBookingBtn.addActionListener(e-> bookingService.showBookings());
        viewVehicleBtn.addActionListener(e-> vehicleService.showVehicles());
        viewDriverBtn.addActionListener(e-> driverService.showDrivers());
        exitBtn.addActionListener(e-> System.exit(0));

        setVisible(true);
    }

    private void loadVehicles() {
        try (Connection conn = DatabaseConnection.getConnection()) {
            PreparedStatement ps = conn.prepareStatement("SELECT vehicle_id, model, rate_per_km FROM Vehicle");
            ResultSet rs = ps.executeQuery();
            while (rs.next()) {
                vehicleBox.addItem(
                    rs.getInt("vehicle_id") + " - " + rs.getString("model") +
                    " (₹" + rs.getDouble("rate_per_km") + "/km)"
                );
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    private void bookVehicle() {
        String name = nameField.getText();
        String phone = phoneField.getText();
        String address = addressField.getText();
        String selectedVehicle = (String) vehicleBox.getSelectedItem();
        String distanceText = distanceField.getText();

        if (name.isEmpty() || phone.isEmpty() || address.isEmpty() || selectedVehicle == null || distanceText.isEmpty()) {
            JOptionPane.showMessageDialog(this, "⚠ Please fill all fields!");
            return;
        }

        try {
            int vehicleId = Integer.parseInt(selectedVehicle.split(" - ")[0]);
            double distance = Double.parseDouble(distanceText);

            double total = bookingService.createBooking(name, phone, address, vehicleId, distance);
            JOptionPane.showMessageDialog(this, "✅ Booking Confirmed! Total: ₹" + total);
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "❌ Error while booking!");
            ex.printStackTrace();
        }
    }

    public static void main(String[] args) {
        new CarRentalGUI();
}
}