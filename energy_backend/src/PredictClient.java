import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

public class PredictClient {
    public static void main(String[] args) {
        try {
            // ✅ Make sure this is your actual JSON path
            String jsonPath = "C:\\Users\\HP\\OneDrive\\Desktop\\energy_consumption\\sample_input.json";

            // Read the latest JSON content
            String jsonInput = new String(Files.readAllBytes(Paths.get(jsonPath)), StandardCharsets.UTF_8);

            // Print to confirm (debug)
            System.out.println("🔍 Sending JSON to Flask: " + jsonInput);

            // Flask API endpoint
            String apiUrl = "http://127.0.0.1:5000/predict";

            // Setup HTTP connection
            URL url = new URL(apiUrl);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/json");
            conn.setDoOutput(true);

            // Send request
            try (OutputStream os = conn.getOutputStream()) {
                byte[] input = jsonInput.getBytes(StandardCharsets.UTF_8);
                os.write(input, 0, input.length);
            }

            // Read response
            BufferedReader br = new BufferedReader(
                new InputStreamReader(conn.getInputStream(), StandardCharsets.UTF_8)
            );
            StringBuilder response = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null) {
                response.append(line.trim());
            }
            br.close();

            // Output the prediction
            System.out.println("✅ Server Response: " + response.toString());

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
