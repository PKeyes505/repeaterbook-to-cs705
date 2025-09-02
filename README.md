# repeaterbook-to-cs705
Convert RepeaterBook CSV exports into a CS-705 compatible CSV for easy repeater programming on the Icom IC-705.

## Instructions

1. Log in to RepeaterBook
   - Visit: https://www.repeaterbook.com/index.php/component/users/login?Itemid=101
   - Sign in to your account.

2. Download Repeater Data
   - Go to: https://www.repeaterbook.com/
   - Select the repeaters you want.
   - Export your selection to CSV format.
   - Save the file as rb.csv for convenience.
     - If you choose another filename, update the code to match.

3. Run the Converter
   - Open a Command Prompt.
   - Navigate to the directory where you saved rb.csv.
   - Run this program.
   - A file named CS-705-Formatted.csv will be created in the same directory.

4. Import into CS-705
   - Open the CS-705 software for the IC-705.
   - Select the repeater group you want to populate.
   - Use the Import function to load CS-705-Formatted.csv.
