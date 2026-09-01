/**
 * ====================================================================
 * 📊 INSPIRE 2026 — OFFICIAL GOOGLE APPS SCRIPT BACKEND
 * Real-Time Leaderboard Synchronization & Registration Pass Dispatch
 * ====================================================================
 * 
 * Instructions:
 * 1. Open your Google Spreadsheet (https://sheets.new).
 * 2. Click Extensions > Apps Script.
 * 3. Replace all content in Code.gs with this entire script.
 * 4. Save (Ctrl+S) and click "Deploy" > "New deployment" (or "Manage deployments" > Edit > New version).
 * 5. Type: "Web app" | Execute as: "Me" | Who has access: "Anyone".
 * 6. Copy the Web App URL and ensure it matches GOOGLE_SHEETS_WEB_APP_URL in admin.html & index.html.
 */

// Default 11 Teams Metadata
const DEFAULT_TEAMS = [
  { id: "team_01", num: "TEAM 01", name: "TEAM CHRONIX", captain: "Veronica Vinutha K", viceCaptain: "Sunidhi Chandra", points: 0 },
  { id: "team_02", num: "TEAM 02", name: "SYNDICATE", captain: "Pavan S", viceCaptain: "Asim Khan", points: 0 },
  { id: "team_03", num: "TEAM 03", name: "QUANTUM PARADOX", captain: "Yuvaraj S", viceCaptain: "Prerana S", points: 0 },
  { id: "team_04", num: "TEAM 04", name: "VERA", captain: "Madhura H K", viceCaptain: "Himani P", points: 0 },
  { id: "team_05", num: "TEAM 05", name: "ERA-X", captain: "Eshwari P", viceCaptain: "Sinchana V", points: 0 },
  { id: "team_06", num: "TEAM 06", name: "ERONX", captain: "Zoya Fathima", viceCaptain: "Simran Bharatiya", points: 0 },
  { id: "team_07", num: "TEAM 07", name: "TIME LOOP", captain: "Harshitha R", viceCaptain: "Adhithi Rashmi D", points: 0 },
  { id: "team_08", num: "TEAM 08", name: "PRABHUTVA", captain: "Hamsa Lakshmi G", viceCaptain: "Ananya R Hakari", points: 0 },
  { id: "team_09", num: "TEAM 09", name: "YUGANTARA", captain: "Yashaswini C", viceCaptain: "Haripriya O", points: 0 },
  { id: "team_10", num: "TEAM 10", name: "EVARA", captain: "Sanjana S Shetty", viceCaptain: "Chinmayi S H", points: 0 },
  { id: "team_11", num: "TEAM 11", name: "CHRONO CREW", captain: "Rishika D", viceCaptain: "Manya R", points: 0 }
];

/**
 * Handles GET requests:
 * - ?action=get_scores : Returns the live 11-team leaderboard scores
 */
function doGet(e) {
  try {
    const action = (e && e.parameter && e.parameter.action) ? e.parameter.action : "get_scores";
    
    if (action === "get_scores") {
      const teams = getLeaderboardScoresFromSheet();
      const response = {
        status: "success",
        teams: teams,
        timestamp: new Date().toLocaleString("en-IN", { timeZone: "Asia/Kolkata" })
      };
      return ContentService.createTextOutput(JSON.stringify(response))
        .setMimeType(ContentService.MimeType.JSON);
    }

    return ContentService.createTextOutput(JSON.stringify({
      status: "success",
      message: "Inspire 2026 Real-Time Live Scoring & Registration API is Online & Ready!"
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      status: "error",
      message: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Handles POST requests:
 * 1. action="update_scores": Admin publishes new points tally to Google Sheets
 * 2. passId / registration: Student submits registration form -> append row & email pass
 */
function doPost(e) {
  try {
    let payload = {};
    if (e && e.postData && e.postData.contents) {
      try {
        payload = JSON.parse(e.postData.contents);
      } catch (jsonErr) {
        payload = e.parameter || {};
      }
    } else if (e && e.parameter) {
      payload = e.parameter;
    }

    // 1. Live Leaderboard Scores Update from Admin
    if (payload.action === "update_scores" && Array.isArray(payload.teams)) {
      saveLeaderboardScoresToSheet(payload.teams, payload.auditLogs || []);
      return ContentService.createTextOutput(JSON.stringify({
        status: "success",
        message: "Live Leaderboard successfully synchronized to Google Cloud!"
      })).setMimeType(ContentService.MimeType.JSON);
    }

    // 2. Student Registration Submission
    if (payload.passId || payload.email || payload.participants) {
      const regResult = handleStudentRegistration(payload);
      return ContentService.createTextOutput(JSON.stringify(regResult))
        .setMimeType(ContentService.MimeType.JSON);
    }

    return ContentService.createTextOutput(JSON.stringify({
      status: "success",
      message: "Data received"
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      status: "error",
      message: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Reads scores from the "Leaderboard" tab in Google Sheets
 */
function getLeaderboardScoresFromSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName("Leaderboard");
  
  if (!sheet) {
    // If sheet doesn't exist yet, initialize it
    initLeaderboardSheet(ss);
    return DEFAULT_TEAMS;
  }

  const data = sheet.getDataRange().getValues();
  if (data.length <= 1) {
    // Header only or empty
    return DEFAULT_TEAMS;
  }

  // Row 1 is header: [Squad ID, Squad Number, Team Name, Points, Captain, Vice Captain, Rank, Last Updated]
  const teams = [];
  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    if (!row[0] && !row[1]) continue;
    teams.push({
      id: String(row[0] || ""),
      num: String(row[1] || ""),
      name: String(row[2] || ""),
      points: Number(row[3]) || 0,
      captain: String(row[4] || ""),
      viceCaptain: String(row[5] || ""),
      rank: Number(row[6]) || i
    });
  }

  return teams.length > 0 ? teams : DEFAULT_TEAMS;
}

/**
 * Saves scores to the "Leaderboard" tab and writes score logs
 */
function saveLeaderboardScoresToSheet(teams, auditLogs) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName("Leaderboard");

  if (!sheet) {
    sheet = ss.insertSheet("Leaderboard");
  }

  sheet.clear();

  // Header row
  const headers = ["Squad ID", "Squad Code", "Team Name", "Total Points", "Captain", "Vice Captain", "Current Rank", "Last Sync Timestamp"];
  sheet.appendRow(headers);

  // Format header
  const headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setFontWeight("bold");
  headerRange.setBackground("#0F172A");
  headerRange.setFontColor("#F8FAFC");
  headerRange.setHorizontalAlignment("center");

  // Sort teams by points descending
  const sorted = [...teams].sort((a, b) => (Number(b.points) || 0) - (Number(a.points) || 0));
  const timeNow = new Date().toLocaleString("en-IN", { timeZone: "Asia/Kolkata" });

  const rows = sorted.map((t, idx) => [
    t.id || "",
    t.num || "",
    t.name || "",
    Number(t.points) || 0,
    t.captain || "",
    t.viceCaptain || "",
    idx + 1,
    timeNow
  ]);

  if (rows.length > 0) {
    sheet.getRange(2, 1, rows.length, headers.length).setValues(rows);
    sheet.getRange(2, 4, rows.length, 1).setFontWeight("bold").setFontColor("#059669");
    sheet.getRange(2, 7, rows.length, 1).setHorizontalAlignment("center");
  }

  sheet.autoResizeColumns(1, headers.length);

  // Optional: write to Score Logs sheet
  if (Array.isArray(auditLogs) && auditLogs.length > 0) {
    let logSheet = ss.getSheetByName("Score Logs");
    if (!logSheet) {
      logSheet = ss.insertSheet("Score Logs");
      const logHeaders = ["Time (IST)", "Team / Squad", "Points Adjustment", "Reason / Event Track", "Type"];
      logSheet.appendRow(logHeaders);
      const lhr = logSheet.getRange(1, 1, 1, logHeaders.length);
      lhr.setFontWeight("bold").setBackground("#1E293B").setFontColor("#FFFFFF");
    }

    const latestLog = auditLogs[0];
    if (latestLog && latestLog.time) {
      logSheet.appendRow([
        latestLog.time,
        latestLog.team || "All Squads",
        latestLog.change || "",
        latestLog.reason || "Manual Point Update",
        latestLog.isPenalty ? "Penalty/Reset" : "Point Award"
      ]);
    }
  }
}

/**
 * Initializes the default leaderboard tab
 */
function initLeaderboardSheet(ss) {
  let sheet = ss.getSheetByName("Leaderboard");
  if (!sheet) {
    sheet = ss.insertSheet("Leaderboard");
  }
  saveLeaderboardScoresToSheet(DEFAULT_TEAMS, []);
}

/**
 * Handles student registration & email dispatch
 */
function handleStudentRegistration(data) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName("Registrations");

  if (!sheet) {
    sheet = ss.insertSheet("Registrations");
    const headers = [
      "Timestamp (IST)",
      "Pass ID",
      "Competition Track",
      "Assigned Squad",
      "Sub-Squad / Duo Alias",
      "Participant Name(s)",
      "Mobile / WhatsApp",
      "College Email ID",
      "Academic Year",
      "Class / Course",
      "Section",
      "Roll Number",
      "Email Pass Status"
    ];
    sheet.appendRow(headers);
    const hr = sheet.getRange(1, 1, 1, headers.length);
    hr.setFontWeight("bold").setBackground("#064E3B").setFontColor("#FFFFFF");
  }

  const timeStr = new Date().toLocaleString("en-IN", { timeZone: "Asia/Kolkata" });
  const passId = data.passId || "INS-" + Math.floor(100000 + Math.random() * 900000);
  const email = (data.email || "").trim();
  let emailStatus = "Skipped (No Email)";

  // Send Email Pass if valid email
  if (email && email.includes("@")) {
    try {
      sendDelegatePassEmail(email, {
        passId: passId,
        participantNames: data.participants || "Registered Delegate",
        trackName: data.event || "Competition Track",
        squadName: data.squad || "Assigned Squad",
        venue: data.venue || "Campus Auditorium",
        timing: data.time || "Reporting: 09:00 AM",
        rollNo: data.rollNo || "N/A"
      });
      emailStatus = "Dispatched Successfully (" + new Date().toLocaleTimeString("en-IN", { timeZone: "Asia/Kolkata" }) + ")";
    } catch (e) {
      emailStatus = "Failed: " + e.toString();
    }
  }

  sheet.appendRow([
    timeStr,
    passId,
    data.event || "",
    data.squad || "",
    data.teamName || "",
    data.participants || "",
    data.phone || "",
    email,
    data.year || "",
    data.course || "",
    data.section || "",
    data.rollNo || "",
    emailStatus
  ]);

  return { status: "success", passId: passId, emailStatus: emailStatus };
}

/**
 * Sends official HTML delegate pass to student
 */
function sendDelegatePassEmail(recipientEmail, info) {
  const subject = `🎟️ Official Entry Pass: ${info.trackName} · ${info.passId} | Inspire 2026`;
  const htmlBody = `
    <div style="font-family: Arial, sans-serif; background-color: #0B101D; color: #F8FAFC; padding: 24px; border-radius: 12px; max-width: 600px; margin: 0 auto; border: 1px solid #1E293B;">
      <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="color: #F59E0B; margin: 0; font-size: 24px; letter-spacing: 2px;">INSPIRE 2026</h1>
        <p style="color: #94A3B8; margin: 4px 0 0 0; font-size: 13px;">ANNUAL INTRA-DEPARTMENT IT EXTRAVAGANZA</p>
      </div>

      <div style="background: linear-gradient(135deg, rgba(245,158,11,0.15), rgba(99,102,241,0.15)); border: 1px solid rgba(245,158,11,0.4); border-radius: 10px; padding: 20px; text-align: center; margin-bottom: 20px;">
        <span style="font-size: 11px; font-family: monospace; color: #F59E0B; letter-spacing: 1px;">VERIFIED ENTRY PASS</span>
        <h2 style="color: #FFFFFF; font-size: 26px; margin: 8px 0; font-family: monospace;">${info.passId}</h2>
        <span style="background: #10B981; color: #064E3B; font-weight: bold; font-size: 11px; padding: 3px 12px; border-radius: 99px;">CONFIRMED</span>
      </div>

      <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 14px;">
        <tr style="border-bottom: 1px solid #1E293B;">
          <td style="padding: 10px 0; color: #94A3B8;">Event Track:</td>
          <td style="padding: 10px 0; color: #38BDF8; font-weight: bold; text-align: right;">${info.trackName}</td>
        </tr>
        <tr style="border-bottom: 1px solid #1E293B;">
          <td style="padding: 10px 0; color: #94A3B8;">Assigned Squad:</td>
          <td style="padding: 10px 0; color: #FBBF24; font-weight: bold; text-align: right;">${info.squadName}</td>
        </tr>
        <tr style="border-bottom: 1px solid #1E293B;">
          <td style="padding: 10px 0; color: #94A3B8;">Delegate(s):</td>
          <td style="padding: 10px 0; color: #FFFFFF; text-align: right;">${info.participantNames}</td>
        </tr>
        <tr style="border-bottom: 1px solid #1E293B;">
          <td style="padding: 10px 0; color: #94A3B8;">Roll Number:</td>
          <td style="padding: 10px 0; color: #FFFFFF; text-align: right;">${info.rollNo}</td>
        </tr>
        <tr style="border-bottom: 1px solid #1E293B;">
          <td style="padding: 10px 0; color: #94A3B8;">Venue:</td>
          <td style="padding: 10px 0; color: #34D399; text-align: right;">${info.venue}</td>
        </tr>
        <tr>
          <td style="padding: 10px 0; color: #94A3B8;">Timing:</td>
          <td style="padding: 10px 0; color: #FCD34D; text-align: right;">${info.timing}</td>
        </tr>
      </table>

      <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 12px; font-size: 12px; color: #94A3B8; line-height: 1.5;">
        ⚠️ <strong>Important Instructions:</strong> Please present this digital pass or your Pass ID at the registration reception upon arrival. All participants must carry their College ID card.
      </div>

      <div style="text-align: center; margin-top: 20px; font-size: 11px; color: #64748B;">
        Inspire 2026 Organizing Committee &middot; Department of Computer Applications
      </div>
    </div>
  `;

  MailApp.sendEmail({
    to: recipientEmail,
    subject: subject,
    htmlBody: htmlBody,
    name: "Inspire 2026 Organizing Desk"
  });
}

/**
 * Test function: Run this once in Apps Script toolbar to authorize email permissions
 */
function testSendEmail() {
  const myEmail = Session.getActiveUser().getEmail();
  if (myEmail) {
    sendDelegatePassEmail(myEmail, {
      passId: "INS-TEST-2026",
      participantNames: "Test Delegate",
      trackName: "IT Quiz (Silicon Brainwave)",
      squadName: "TEAM 01 · TEAM CHRONIX",
      venue: "Main Auditorium",
      timing: "09:00 AM - 10:30 AM",
      rollNo: "26BCA001"
    });
    Logger.log("Test pass email sent successfully to: " + myEmail);
  } else {
    Logger.log("No active user email detected.");
  }
}
