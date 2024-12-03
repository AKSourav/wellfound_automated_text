# Wellfound Messenger Bot

An automated messaging tool for Wellfound (formerly AngelList Talent) that uses Selenium WebDriver for sending messages through the platform.

## Features

- Cookie-based authentication
- Automated message sending
- Configurable recipient and message content
- Error handling with screenshot capture
- Headless mode support (optional)

## Prerequisites

- Python 3.x
- Google Chrome browser
- ChromeDriver (matching your Chrome version)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AKSourav/wellfound_automated_text.git
   cd wellfound_automated_text
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create environment files:

   Create a `.env` file based on the `.env.sample`:
   ```
   RECIPIENT_URL=https://wellfound.com/jobs/messages/<message-id>
   MESSAGE=Your message here
   ```

4. Set up cookies:

   Create a `cookies.json` file with your Wellfound authentication cookies. You can obtain these by:
   - Logging into Wellfound in Chrome
   - Using a browser extension to export cookies
   - Saving them in the following format:
     ```json
     [
       {
         "domain": ".wellfound.com",
         "name": "cookie_name",
         "value": "cookie_value",
         "path": "/",
         "secure": true,
         "httpOnly": true,
         "expiry": 1234567890
       }
     ]
     ```

## Usage

Run the script:
   ```bash
   python main.py
   ```

The script will:
1. Initialize a Chrome browser session
2. Load your authentication cookies
3. Verify login status
4. Navigate to the recipient's profile
5. Send the configured message
6. Close the browser

## Configuration Options

### Headless Mode

To run the browser in headless mode (without UI), uncomment this line in `main.py`:
   ```python
   # chrome_options.add_argument('--headless')
   ```

### Debug Mode

The script automatically saves screenshots on errors to `error_screenshot.png` for debugging purposes.

## Error Handling

The script includes several error handling features:
- Login verification
- Cookie validation
- Screenshot capture on errors
- Detailed error logging

## Project Structure

├── main.py              # Main script
├── .env                 # Environment variables
├── .env.sample         # Environment variables template
├── cookies.json        # Authentication cookies
└── requirements.txt    # Python dependencies
