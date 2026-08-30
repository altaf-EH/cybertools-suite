import re
import sys
import os
import requests
import ipaddress
from datetime import datetime
from dotenv import load_dotenv
from collections import defaultdict
load_dotenv()

ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY")

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.utils import ImageReader


# ============================================================
# CONFIGURATION
# ============================================================

REPORT_DIR = "reports"
# Supported file extensions
SUPPORTED_EXTENSIONS = {".log", ".txt"}


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def generate_report(filename):
    c = canvas.Canvas(filename)
    c.setAuthor("CyberTools")
    c.setCreator("CyberTools Log Analyzer")
    c.setTitle("Log Analysis Report")

    c.save()

def get_log_path():
    """Get log file path from command line or user input."""
    positional_args = [
        arg for arg in sys.argv[1:]
        if not arg.startswith("--")
    ]

    if positional_args:
        return positional_args[0].strip().strip('"').strip("'")

    print()
    print("=" * 60)
    print("                    LOG ANALYZER")
    print("=" * 60)
    print()

    return input("Enter log file path: ").strip().strip('"').strip("'")

def get_output_dir():
    """Read --output flag from command line. Falls back to default."""
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            return sys.argv[idx + 1].strip().strip('"').strip("'")
    return REPORT_DIR

def validate_file(file_path):
    """Check if file exists and has supported extension."""
    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        sys.exit(1)
    
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        print(f"[ERROR] Unsupported file format: {ext}")
        print("Supported formats: .log, .txt,")
        sys.exit(1)
    
    return True

def check_args():
    # Agar koi bina bataye tool chalaye aur aapko check karna ho:
    if "--credits" in sys.argv:
        print("\n==================================================")
        print("[+] Tool Name: CyberTools Log Analyzer")
        print("[+] Developer: CyberTools Team (c) 2026")
        print("[+] License  : Creative Commons BY-NC-ND 4.0")
        print("==================================================")
        sys.exit(0)

def is_valid_ip(ip):
    """Check whether a string is a valid IP address."""

    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def is_private_ip(ip):
    """Determine whether an IP is private/local."""

    try:
        address = ipaddress.ip_address(ip)

        return (
            address.is_private
            or address.is_loopback
            or address.is_link_local
            or address.is_reserved
        )

    except ValueError:
        return False


def get_ip_intelligence(ip):
    """Get public IP information from ip-api.com."""

    if is_private_ip(ip):
        return {
            "status": "private",
            "country": "Private/Local",
            "country_code": "-",
            "region": "-",
            "city": "-",
            "zip": "-",
            "timezone": "-",
            "isp": "-",
            "org": "-",
            "asn": "-"
        }

    try:
        response = requests.get(
            f"http://ip-api.com/json/{ip}",
            params={
                "fields": (
                    "status,country,countryCode,region,regionName,"
                    "city,zip,timezone,isp,org,as,query"
                )
            },
            timeout=5
        )

        data = response.json()

        if data.get("status") != "success":
            return {
                "status": "failed",
                "country": "N/A",
                "country_code": "-",
                "region": "-",
                "city": "-",
                "zip": "-",
                "timezone": "-",
                "isp": "N/A",
                "org": "N/A",
                "asn": "N/A"
            }

        return {
            "status": "success",
            "country": data.get("country", "N/A"),
            "country_code": data.get("countryCode", "-"),
            "region": data.get("regionName", "N/A"),
            "city": data.get("city", "N/A"),
            "zip": data.get("zip", "N/A"),
            "timezone": data.get("timezone", "N/A"),
            "isp": data.get("isp", "N/A"),
            "org": data.get("org", "N/A"),
            "asn": data.get("as", "N/A")
        }

    except requests.RequestException:
        return {
            "status": "failed",
            "country": "N/A",
            "country_code": "-",
            "region": "-",
            "city": "-",
            "zip": "-",
            "timezone": "-",
            "isp": "N/A",
            "org": "N/A",
            "asn": "N/A"
        }

def get_abuseipdb_intelligence(ip):
    """Get abuse reputation information from AbuseIPDB."""

    if is_private_ip(ip):
        return {
            "status": "private",
            "abuse_confidence": "N/A",
            "total_reports": "N/A",
            "last_reported": "N/A",
            "categories": "N/A"
        }

    if not ABUSEIPDB_API_KEY:
        return {
            "status": "no_api_key",
            "abuse_confidence": "N/A",
            "total_reports": "N/A",
            "last_reported": "N/A",
            "categories": "N/A"
        }

    url = "https://api.abuseipdb.com/api/v2/check"

    headers = {
        "Accept": "application/json",
        "Key": ABUSEIPDB_API_KEY
    }

    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json().get("data", {})

        categories = data.get("reports", [])

        return {
            "status": "success",
            "abuse_confidence": data.get(
                "abuseConfidenceScore",
                "N/A"
            ),
            "total_reports": data.get(
                "totalReports",
                "N/A"
            ),
            "last_reported": data.get(
                "lastReportedAt",
                "N/A"
            ),
            "categories": categories
        }

    except requests.RequestException as error:

        return {
            "status": "failed",
            "abuse_confidence": "N/A",
            "total_reports": "N/A",
            "last_reported": "N/A",
            "categories": "N/A"
        }

def format_duration(seconds):
    """Convert seconds into a readable duration."""

    seconds = int(seconds)

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60

    if hours > 0:
        return f"{hours}h {minutes}m {remaining_seconds}s"

    if minutes > 0:
        return f"{minutes}m {remaining_seconds}s"

    return f"{remaining_seconds}s"


def calculate_attack_speed(attempts, duration_seconds):
    """Calculate attack speed and return label + rate."""

    if duration_seconds <= 0:
        rate = float(attempts)
    else:
        rate = attempts / duration_seconds

    if rate > 10:
        label = "VERY FAST"
    elif rate > 2:
        label = "FAST"
    elif rate > 0.5:
        label = "SLOW"
    else:
        label = "VERY SLOW"

    return label, rate

# Core parsing logic - Protected under CyberTools Signature

def calculate_risk(attempts, username_count, speed_label):
    """Calculate a simple local behavioral risk score."""

    score = 0
    reasons = []

    # Attempt volume
    if attempts >= 50:
        score += 40
        reasons.append("Very high number of failed login attempts.")
    elif attempts >= 20:
        score += 30
        reasons.append("High number of failed login attempts.")
    elif attempts >= 7:
        score += 20
        reasons.append("Repeated failed login attempts detected.")
    elif attempts >= 4:
        score += 10
        reasons.append("Multiple failed login attempts detected.")
    else:
        reasons.append("Low number of failed login attempts.")

    # Multiple accounts
    if username_count >= 5:
        score += 25
        reasons.append("Multiple user accounts were targeted.")
    elif username_count >= 3:
        score += 15
        reasons.append("Several user accounts were targeted.")
    else:
        reasons.append("Limited number of accounts targeted.")

    # Attack speed
    if speed_label == "VERY FAST":
        score += 25
        reasons.append("Attack activity appears highly automated.")
    elif speed_label == "FAST":
        score += 15
        reasons.append("Attack speed is unusually high.")
    elif speed_label == "SLOW":
        score += 5
        reasons.append("Slow but repeated suspicious activity.")
    else:
        reasons.append("Attack activity is currently very slow.")

    if score >= 60:
        risk = "HIGH"
    elif score >= 30:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return risk, score, reasons


# ============================================================
# LOG PARSER
# ============================================================

def parse_log(log_path):
    """
    FUTURE-PROOF LOG PARSER
    - Keywords par depend nahi karta
    - Har line se IP + Username + Time nikalta hai (agar mila toh)
    - Agar kuch nahi mila toh bhi crash nahi karega
    """
    
    import re
    from collections import defaultdict
    
    # Data store karne ke liye
    ip_data = defaultdict(lambda: {
        'count': 0,
        'usernames': set(),
        'timestamps': [],
        'line_samples': []  # Debug ke liye
    })
    
    total_lines = 0
    lines_with_ip = 0
    
    try:
        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                total_lines += 1
                
                # ----------------------------------------------------
                # STEP 1: IP ADDRESS DHUNDO (HAR LINE MEIN)
                # Yeh regex har tarah ke IP ko pakadta hai (IPv4)
                # ----------------------------------------------------
                ip_match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', line)
                if not ip_match:
                    continue  # Agar IP nahi hai toh skip, kyunki log analysis IP ke bina meaningless hai
                
                lines_with_ip += 1
                ip = ip_match.group()
                
                # ----------------------------------------------------
                # STEP 2: TIME DHUNDO (KISI BHI FORMAT MEIN)
                # 12:34:56  OR  12:34:56.789  OR  [12:34:56]
                # ----------------------------------------------------
                time_match = re.search(r'(\d{2}:\d{2}:\d{2}(?:\.\d+)?)', line)
                timestamp = time_match.group(1) if time_match else "unknown"
                
                # ----------------------------------------------------
                # STEP 3: USERNAME DHUNDO (GENERIC)
                # "user xyz", "for xyz", "login: xyz", "account=xyz",
                # "username: xyz", "from xyz", "xyz@domain"
                # ----------------------------------------------------
                username = "unknown"
                
                # Pattern 1: Standard "user xyz" ya "for xyz"
                user_match = re.search(r'(?:user|for|login:|username:|account=|\s)([a-zA-Z0-9_\-@.]+)', line, re.IGNORECASE)
                if user_match:
                    username = user_match.group(1)
                else:
                    # Pattern 2: Email format (xyz@domain.com)
                    email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', line)
                    if email_match:
                        username = email_match.group(1)
                    else:
                        # Pattern 3: Kuch bhi jo alphanumeric + special chars ho (fallback)
                        fallback_match = re.search(r'\b([a-zA-Z0-9_\-]{3,20})\b', line)
                        if fallback_match:
                            # Agar common words (root, admin, bin) nahi hain toh username maan lo
                            common_words = {'root', 'admin', 'bin', 'daemon', 'sys', 'sync', 'shutdown', 'halt', 'mail'}
                            if fallback_match.group(1).lower() not in common_words:
                                username = fallback_match.group(1)
                
                # ----------------------------------------------------
                # STEP 4: STORE DATA
                # ----------------------------------------------------
                ip_data[ip]['count'] += 1
                ip_data[ip]['usernames'].add(username)
                ip_data[ip]['timestamps'].append(timestamp)
                
                # Debug ke liye pehli 5 lines store karo
                if len(ip_data[ip]['line_samples']) < 5:
                    ip_data[ip]['line_samples'].append(line.strip()[:100])
    
    except Exception as e:
        print(f"[!] Warning: Log reading mein issue: {e}")
        # Agar kuch bhi ho, crash mat karo
    
    # ----------------------------------------------------------------
    # STEP 5: DATA CLEANUP AUR ANALYSIS
    # ----------------------------------------------------------------
    
    # Agar kisi IP ne sirf 1-2 baar attempt kiya hai, ignore karo (noise)
    filtered_data = {
        ip: data for ip, data in ip_data.items()
        if data['count'] >= 3  # Minimum 3 attempts
    }
    
    # Agar kuch nahi mila, toh empty return karo (crash nahi hoga)
    if not filtered_data:
        print("[!] No significant IP activity found in this log.")
        return {
            'total_events': total_lines,
            'ip_results': [],
            'summary': 'No suspicious activity detected.'
        }
    
    # Results prepare karo
    results = []
    for ip, data in filtered_data.items():
        # 🔥 Calculate duration if timestamps available
        duration_text = 'N/A'
        if len(data['timestamps']) >= 2:
            try:
                first = data['timestamps'][0]
                last = data['timestamps'][-1]
                # Convert string times to datetime
                from datetime import datetime
                t1 = datetime.strptime(first, '%H:%M:%S')
                t2 = datetime.strptime(last, '%H:%M:%S')
                if t2 < t1:
                    from datetime import timedelta
                    t2 += timedelta(days=1)
                seconds = (t2 - t1).total_seconds()
                duration_text = format_duration(seconds)
            except:
                duration_text = 'N/A'
        
        results.append({
            'ip': ip,
            'attempts': data['count'],
            'unique_usernames': len(data['usernames']),
            'usernames': list(data['usernames'])[:5],
            'first_seen': data['timestamps'][0] if data['timestamps'] else 'N/A',
            'last_seen': data['timestamps'][-1] if data['timestamps'] else 'N/A',
            'sample_lines': data['line_samples'],
            # 🔥 ADD ALL MISSING KEYS:
            'duration': duration_text,
            'attempts_per_second': 0.0,
            'abuse_intelligence': {
                'abuse_confidence': 'N/A',
                'total_reports': 'N/A',
                'last_reported': 'N/A'
            },
            'intelligence': {
                'country': 'N/A',
                'region': 'N/A',
                'city': 'N/A',
                'isp': 'N/A',
                'org': 'N/A',
                'asn': 'N/A'
            },
            'risk_score': 0,
            'risk': 'LOW',
            'ip_type': 'PUBLIC',
            'speed': 'SLOW',
            'reasons': ['No suspicious activity detected']
        })
    
    # Sort by attempts (highest first)
    results.sort(key=lambda x: x['attempts'], reverse=True)
    
    for idx, result in enumerate(results, start=1):
        result['rank'] = idx

    return {
        'total_events': total_lines,
        'total_unique_ips': len(results),
        'ip_results': results,
        'summary': f"Found {len(results)} suspicious IPs with {sum(r['attempts'] for r in results)} total events."
    }

# ============================================================
# IP ANALYSIS
# ============================================================

def analyze_ips(
    ip_counts,
    ip_usernames,
    attack_user_counts,
    ip_attack_times
):

    sorted_ips = sorted(
        ip_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )

    ip_results = []

    for rank, (ip, attempts) in enumerate(sorted_ips, start=1):

        first_seen = ip_attack_times[ip]["first"]
        last_seen = ip_attack_times[ip]["last"]

        duration_seconds = 0
        duration_text = "unknown"

        if first_seen != "unknown" and last_seen != "unknown":

            try:

                start_time = datetime.strptime(
                    first_seen,
                    "%H:%M:%S"
                )

                end_time = datetime.strptime(
                    last_seen,
                    "%H:%M:%S"
                )

                # Handle attacks crossing midnight
                if end_time < start_time:
                    from datetime import timedelta
                    end_time += timedelta(days=1)

                duration_seconds = (
                    end_time - start_time
                ).total_seconds()

                duration_text = format_duration(
                    duration_seconds
                )

            except ValueError:

                duration_seconds = 0
                duration_text = "unknown"

        speed_label, attempts_per_second = calculate_attack_speed(
            attempts,
            duration_seconds
        )

        username_count = len(
            attack_user_counts.get(ip, {})
        )

        risk, risk_score, reasons = calculate_risk(
            attempts,
            username_count,
            speed_label
        )

        usernames = []

        for username, username_attempts in (
            attack_user_counts.get(ip, {}).items()
        ):
            usernames.append(
                f"{username} ({username_attempts})"
            )

        ip_type = (
            "PRIVATE / LOCAL"
            if is_private_ip(ip)
            else "PUBLIC"
        )

        ip_intelligence = get_ip_intelligence(ip)
        abuse_intelligence = get_abuseipdb_intelligence(ip)
        ip_results.append(
            {
                "rank": rank,
                "ip": ip,
                "attempts": attempts,
                "risk": risk,
                "risk_score": risk_score,
                "first_seen": first_seen,
                "last_seen": last_seen,
                "duration": duration_text,
                "duration_seconds": duration_seconds,
                "speed": speed_label,
                "attempts_per_second": attempts_per_second,
                "usernames": usernames,
                "username_count": username_count,
                "ip_type": ip_type,
                "reasons": reasons,
                "intelligence": ip_intelligence,
                "abuse_intelligence": abuse_intelligence
            }
        )

    return ip_results


# ============================================================
# OVERALL RISK
# ============================================================

def calculate_overall_risk(total_attempts, unique_ips, ip_results):
    if not ip_results:
        return "LOW", ["No suspicious IP activity detected."]
    
    # 🔥 FIX: Check if 'risk_score' exists in each result
    try:
        highest_score = max(result.get('risk_score', 0) for result in ip_results)
    except:
        highest_score = 0
    
    reasons = []
    
    if total_attempts >= 100:
        reasons.append("Large number of failed authentication attempts detected.")
    elif total_attempts >= 30:
        reasons.append("Moderate-to-high authentication activity detected.")
    else:
        reasons.append("Overall failed authentication volume is relatively low.")
    
    if unique_ips >= 10:
        reasons.append("Large number of unique source IP addresses detected.")
    elif unique_ips >= 5:
        reasons.append("Multiple source IP addresses detected.")
    
    if highest_score >= 60:
        overall_risk = "HIGH"
    elif highest_score >= 30:
        overall_risk = "MEDIUM"
    else:
        overall_risk = "LOW"
    
    return overall_risk, reasons


# ============================================================
# TERMINAL REPORT
# ============================================================

def print_terminal_report(
    report_time,
    total_attempts,
    unique_ips,
    overall_risk,
    overall_reasons,
    ip_results
):

    print()
    print("=" * 100)
    print("                         LOG ANALYSIS REPORT")
    print("=" * 100)

    print(f"Generated On          : {report_time}")
    print(f"Total Failed Attempts : {total_attempts}")
    print(f"Unique Source IPs     : {unique_ips}")
    print(f"Overall Risk          : {overall_risk}")

    print()
    print("Overall Risk Reasons:")

    for reason in overall_reasons:
        print(f"  • {reason}")

    print()
    print("=" * 100)
    print("                         SUSPICIOUS IPS")
    print("=" * 100)

    print(
        f"{'Rank':<6}"
        f"{'IP Address':<18}"
        f"{'Attempts':<10}"
        f"{'Risk':<10}"
        f"{'Type':<18}"
        f"{'Speed':<12}"
    )

    print("-" * 100)

    for idx, result in enumerate(ip_results, start=1):
        print(
            f"{idx:<6}"  # 🔥 rank ki jagah idx use karo
            f"{result['ip']:<18}"
            f"{result['attempts']:<10}"
            f"{result.get('risk', 'LOW'):<10}"
            f"{result.get('ip_type', 'PUBLIC'):<18}"
            f"{result.get('speed', 'SLOW'):<12}"
        )

        print(
            f"      First Seen : {result['first_seen']}"
        )

        print(
            f"      Last Seen  : {result['last_seen']}"
        )

        print(
            f"      Duration   : {result['duration']}"
        )

        print(
            f"      Rate       : "
            f"{result['attempts_per_second']:.2f} attempts/sec"
        )

        abuse = result["abuse_intelligence"]

        print(
            f"      Abuse Confidence : "
            f"{abuse['abuse_confidence']}%"
        )

        print(
            f"      Abuse Reports    : "
            f"{abuse['total_reports']}"
        )

        print(
            f"      Last Reported    : "
            f"{abuse['last_reported']}"
        )

        intelligence = result["intelligence"]

        print(
            f"      Country    : {intelligence['country']}"
        )

        print(
            f"      Region     : {intelligence['region']}"
        )

        print(
            f"      City       : {intelligence['city']}"
        )

        print(
            f"      ISP        : {intelligence['isp']}"
        )

        print(
            f"      Organization: {intelligence['org']}"
        )

        print(
            f"      ASN        : {intelligence['asn']}"
        )

        print(
            f"      Usernames  : "
            f"{', '.join(result['usernames'])}"
        )

        print(
            f"      Risk Score : {result['risk_score']}/90"
        )

        print("      Reasons:")

        for reason in result["reasons"]:
            print(f"        • {reason}")

        print()

    print("=" * 100)

# ============================================================
# PDF HELPERS
# ============================================================

PDF_NAVY = HexColor("#102A43")
PDF_BLUE = HexColor("#168AAD")
PDF_LIGHT_BLUE = HexColor("#EAF4FB")
PDF_BORDER = HexColor("#C9D6E2")
PDF_TEXT = HexColor("#1F2933")
PDF_MUTED = HexColor("#52606D")
PDF_GREEN = HexColor("#16804B")
PDF_ORANGE = HexColor("#D97706")
PDF_RED = HexColor("#C0392B")
PDF_LIGHT_GREEN = HexColor("#EAF7EF")
PDF_LIGHT_ORANGE = HexColor("#FFF4E5")
PDF_LIGHT_RED = HexColor("#FDECEC")


# ============================================================
# CYBERTOOLS LOGO
# ============================================================

LOGO_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "assets",
    "cybertools_logo1.png"
)


def draw_cybertools_logo(pdf, x, y, width=145):
    """
    Draw the official CyberTools PNG logo.
    The source path is relative to this project, so the logo
    continues to work when the repository is cloned elsewhere.
    """

    if not os.path.exists(LOGO_PATH):
        print()
        print("[ERROR] CyberTools logo not found:")
        print(LOGO_PATH)
        print()
        return

    image = ImageReader(LOGO_PATH)

    image_width, image_height = image.getSize()

    aspect_ratio = image_height / image_width

    height = width * aspect_ratio

    pdf.drawImage(
        image,
        x,
        y - height,
        width=width,
        height=height,
        preserveAspectRatio=True,
        mask="auto"
    )


def draw_pdf_header(pdf, width, height, page_no):
    """
    Draw a clean CyberTools header on every page.
    """

    # --------------------------------------------------------
    # OFFICIAL CYBERTOOLS LOGO
    # --------------------------------------------------------

    draw_cybertools_logo(
        pdf,
        45,
        height - 18,
        width=110
    )

    # --------------------------------------------------------
    # PAGE NUMBER
    # --------------------------------------------------------

    pdf.setFont(
        "Helvetica-Bold",
        7
    )

    pdf.setFillColor(
        PDF_MUTED
    )

    pdf.drawRightString(
        width - 45,
        height - 28,
        f"PAGE {page_no}"
    )

    # --------------------------------------------------------
    # HEADER DIVIDER
    # --------------------------------------------------------

    pdf.setStrokeColor(
        PDF_BLUE
    )

    pdf.setLineWidth(
        1.0
    )

    pdf.line(
        45,
        height - 70,
        width - 45,
        height - 70
    )


def draw_pdf_footer(pdf, width):
    """
    Draw consistent footer.
    """

    pdf.setStrokeColor(PDF_BORDER)
    pdf.setLineWidth(0.7)

    pdf.line(
        45,
        38,
        width - 45,
        38
    )

    pdf.setFont("Helvetica", 7)
    pdf.setFillColor(PDF_MUTED)

    pdf.drawString(
        45,
        25,
        "CyberTools Log Analyzer"
    )

    pdf.drawRightString(
        width - 45,
        25,
        "Defensive Security Analysis"
    )


def pdf_start_new_page(pdf, width, height, page_no):
    """
    Start a new page and redraw the standard header.
    """

    draw_pdf_footer(pdf, width)
    pdf.showPage()

    page_no += 1

    draw_pdf_header(
        pdf,
        width,
        height,
        page_no
    )

    return page_no, height - 88


def pdf_ensure_space(
    pdf,
    y,
    required_height,
    width,
    height,
    page_no
):
    """
    Ensure enough vertical space exists before drawing content.
    """

    if y - required_height < 55:

        page_no, y = pdf_start_new_page(
            pdf,
            width,
            height,
            page_no
        )

    return page_no, y

# Core parsing logic - Protected under CyberTools Signature

def pdf_draw_wrapped_text(
    pdf,
    text,
    x,
    y,
    max_width,
    font="Helvetica",
    size=8,
    leading=11
):
    """
    Draw text with simple word wrapping.
    """

    pdf.setFont(font, size)
    pdf.setFillColor(PDF_TEXT)

    words = str(text).split()

    lines = []
    current = ""

    for word in words:

        test = (
            word
            if not current
            else current + " " + word
        )

        if stringWidth(
            test,
            font,
            size
        ) <= max_width:

            current = test

        else:

            if current:
                lines.append(current)

            current = word

    if current:
        lines.append(current)

    for line in lines:

        pdf.drawString(
            x,
            y,
            line
        )

        y -= leading

    return y


def pdf_draw_section_title(
    pdf,
    title,
    x,
    y,
    width
):
    """
    Draw a professional section heading.
    """

    pdf.setFillColor(PDF_NAVY)

    pdf.roundRect(
        x,
        y - 16,
        width,
        18,
        3,
        fill=1,
        stroke=0
    )

    pdf.setFont(
        "Helvetica-Bold",
        9
    )

    pdf.setFillColor(white)

    pdf.drawString(
        x + 8,
        y - 11,
        title
    )

    return y - 27


def pdf_draw_info_row(
    pdf,
    fields,
    x,
    y,
    width,
    columns=2
):
    """
    Draw compact information fields in a grid.
    """

    gap = 7

    total_gap = gap * (columns - 1)

    cell_width = (
        width - total_gap
    ) / columns

    cell_height = 34

    rows = []

    for index in range(
        0,
        len(fields),
        columns
    ):

        rows.append(
            fields[
                index:index + columns
            ]
        )

    for row in rows:

        for col_index, field in enumerate(row):

            label, value = field

            cell_x = (
                x
                + col_index
                * (cell_width + gap)
            )

            pdf.setFillColor(
                HexColor("#F7FAFC")
            )

            pdf.setStrokeColor(
                PDF_BORDER
            )

            pdf.setLineWidth(0.6)

            pdf.roundRect(
                cell_x,
                y - cell_height,
                cell_width,
                cell_height,
                3,
                fill=1,
                stroke=1
            )

            pdf.setFont(
                "Helvetica-Bold",
                6.8
            )

            pdf.setFillColor(
                PDF_MUTED
            )

            pdf.drawString(
                cell_x + 7,
                y - 11,
                label.upper()
            )

            pdf.setFont(
                "Helvetica-Bold",
                8
            )

            pdf.setFillColor(
                PDF_TEXT
            )

            value_text = str(value)

            if len(value_text) > 30:
                value_text = (
                    value_text[:27]
                    + "..."
                )

            pdf.drawString(
                cell_x + 7,
                y - 25,
                value_text
            )

        y -= (
            cell_height
            + gap
        )

    return y


def pdf_draw_risk_badge(
    pdf,
    risk,
    x,
    y
):
    """
    Draw HIGH / MEDIUM / LOW badge.
    """

    if risk == "HIGH":

        fill = PDF_LIGHT_RED
        text_color = PDF_RED

    elif risk == "MEDIUM":

        fill = PDF_LIGHT_ORANGE
        text_color = PDF_ORANGE

    else:

        fill = PDF_LIGHT_GREEN
        text_color = PDF_GREEN

    badge_width = 58
    badge_height = 18

    pdf.setFillColor(fill)
    pdf.setStrokeColor(text_color)

    pdf.roundRect(
        x,
        y - badge_height,
        badge_width,
        badge_height,
        5,
        fill=1,
        stroke=1
    )

    pdf.setFont(
        "Helvetica-Bold",
        7.5
    )

    pdf.setFillColor(
        text_color
    )

    pdf.drawCentredString(
        x + badge_width / 2,
        y - 12,
        risk
    )


# ============================================================
# PDF REPORT
# ============================================================

def generate_pdf_report(
    path,
    report_time,
    total_attempts,
    unique_ips,
    overall_risk,
    overall_reasons,
    ip_results
):

    pdf = canvas.Canvas(
        path,
        pagesize=A4
    )

    width, height = A4

    page_no = 1

    draw_pdf_header(
        pdf,
        width,
        height,
        page_no
    )

    y = height - 94

    # --------------------------------------------------------
    # REPORT TITLE
    # --------------------------------------------------------

    pdf.setFont(
        "Helvetica-Bold",
        15
    )

    pdf.setFillColor(
        PDF_TEXT
    )

    pdf.drawString(
        45,
        y,
        "LOG ANALYSIS REPORT"
    )

    y -= 17

    pdf.setFont(
        "Helvetica",
        8
    )

    pdf.setFillColor(
        PDF_MUTED
    )

    pdf.drawString(
        45,
        y,
        f"Generated: {report_time}"
    )

    y -= 25

    # --------------------------------------------------------
    # SUMMARY CARDS
    # --------------------------------------------------------

    card_gap = 8

    card_width = (
        width
        - 90
        - (card_gap * 2)
    ) / 3

    card_height = 54

    summary = [
        (
            "FAILED ATTEMPTS",
            str(total_attempts)
        ),
        (
            "SOURCE IPS",
            str(unique_ips)
        ),
        (
            "OVERALL RISK",
            overall_risk
        )
    ]

    for index, (label, value) in enumerate(summary):

        card_x = (
            45
            + index
            * (card_width + card_gap)
        )

        pdf.setFillColor(
            PDF_LIGHT_BLUE
        )

        pdf.setStrokeColor(
            PDF_BORDER
        )

        pdf.roundRect(
            card_x,
            y - card_height,
            card_width,
            card_height,
            5,
            fill=1,
            stroke=1
        )

        pdf.setFont(
            "Helvetica-Bold",
            6.8
        )

        pdf.setFillColor(
            PDF_MUTED
        )

        pdf.drawString(
            card_x + 9,
            y - 15,
            label
        )

        pdf.setFont(
            "Helvetica-Bold",
            15
        )

        if label == "OVERALL RISK":

            if overall_risk == "HIGH":
                pdf.setFillColor(PDF_RED)

            elif overall_risk == "MEDIUM":
                pdf.setFillColor(PDF_ORANGE)

            else:
                pdf.setFillColor(PDF_GREEN)

        else:

            pdf.setFillColor(
                PDF_NAVY
            )

        pdf.drawString(
            card_x + 9,
            y - 38,
            value
        )

    y -= card_height + 18

    # --------------------------------------------------------
    # OVERALL RISK REASONS
    # --------------------------------------------------------

    y = pdf_draw_section_title(
        pdf,
        "OVERALL RISK ASSESSMENT",
        45,
        y,
        width - 90
    )

    for reason in overall_reasons:

        page_no, y = pdf_ensure_space(
            pdf,
            y,
            18,
            width,
            height,
            page_no
        )

        pdf.setFont(
            "Helvetica",
            8
        )

        pdf.setFillColor(
            PDF_TEXT
        )

        pdf.drawString(
            55,
            y,
            "•"
        )

        y = pdf_draw_wrapped_text(
            pdf,
            reason,
            67,
            y,
            width - 122,
            size=8,
            leading=10
        )

        y -= 2

    y -= 8

    # --------------------------------------------------------
    # SUSPICIOUS IP ANALYSIS
    # --------------------------------------------------------

    # Keep page 1 as the executive summary.
    # Detailed IP analysis starts on page 2.

    draw_pdf_footer(
        pdf,
        width
    )

    pdf.showPage()

    page_no += 1

    draw_pdf_header(
        pdf,
        width,
        height,
        page_no
    )

    y = height - 88

    y = pdf_draw_section_title(
        pdf,
        "SUSPICIOUS IP ANALYSIS",
        45,
        y,
        width - 90
    )

    for result in ip_results:

        # Give each IP block enough starting space.
        page_no, y = pdf_ensure_space(
            pdf,
            y,
            540,
            width,
            height,
            page_no
        )

        # ----------------------------------------------------
        # IP HEADER
        # ----------------------------------------------------

        pdf.setFillColor(
            PDF_NAVY
        )

        pdf.roundRect(
            45,
            y - 28,
            width - 90,
            28,
            5,
            fill=1,
            stroke=0
        )

        pdf.setFont(
            "Helvetica-Bold",
            11
        )

        pdf.setFillColor(
            white
        )

        pdf.drawString(
            55,
            y - 18,
            f"#{result['rank']}  {result['ip']}"
        )

        # Risk score + risk badge
        pdf.setFont(
            "Helvetica-Bold",
            7
        )

        pdf.setFillColor(PDF_MUTED)

        pdf.drawRightString(
            width - 135,
            y - 10,
            "RISK SCORE"
        )

        pdf.setFont(
            "Helvetica-Bold",
            11
        )

        pdf.setFillColor(white)

        pdf.drawRightString(
            width - 135,
            y - 22,
            f"{result.get('risk_score', 0)}/90")

        pdf_draw_risk_badge(
            pdf,
            result["risk"],
            width - 115,
            y - 5
        )

        y -= 40

        # ----------------------------------------------------
        # BASIC INFORMATION
        # ----------------------------------------------------

        fields = [
            (
                "IP Type",
                result["ip_type"]
            ),
            (
                "Attempts",
                result["attempts"]
            ),
            (
                "First Seen",
                result["first_seen"]
            ),
            (
                "Last Seen",
                result["last_seen"]
            ),
            (
                "Duration",
                result["duration"]
            ),
            (
                "Attack Speed",
                result["speed"]
            ),
            (
                "Attempts / Second",
                f"{result['attempts_per_second']:.2f}"
            ),
            (
                "Abuse Confidence",
                f"{result['abuse_intelligence']['abuse_confidence']}%"
            ),
            (
                "Abuse Reports",
                result["abuse_intelligence"]["total_reports"]
            ),
            (
                "Last Reported",
                result["abuse_intelligence"]["last_reported"]
            ),
            (
                "Country",
                result["intelligence"]["country"]
            ),
            (
                "Region",
                result["intelligence"]["region"]
            ),
            (
                "City",
                result["intelligence"]["city"]
            ),
            (
                "ISP",
                result["intelligence"]["isp"]
            ),
            (
                "Organization",
                result["intelligence"]["org"]
            ),
            (
                "ASN",
                result["intelligence"]["asn"]
            )
        ]

        page_no, y = pdf_ensure_space(
            pdf,
            y,
            150,
            width,
            height,
            page_no
        )

        y = pdf_draw_info_row(
            pdf,
            fields,
            45,
            y,
            width - 90,
            columns=2
        )

        # ----------------------------------------------------
        # TARGETED USERNAMES
        # ----------------------------------------------------

        page_no, y = pdf_ensure_space(
            pdf,
            y,
            55,
            width,
            height,
            page_no
        )

        y = pdf_draw_section_title(
            pdf,
            "TARGETED USERNAMES",
            45,
            y,
            width - 90
        )

        username_text = (
            ", ".join(
                result["usernames"]
            )
            if result["usernames"]
            else "None detected"
        )

        y = pdf_draw_wrapped_text(
            pdf,
            username_text,
            55,
            y,
            width - 110,
            size=8,
            leading=11
        )

        y -= 8

        # ----------------------------------------------------
        # ANALYSIS REASONS
        # ----------------------------------------------------

        page_no, y = pdf_ensure_space(
            pdf,
            y,
            55,
            width,
            height,
            page_no
        )

        y = pdf_draw_section_title(
            pdf,
            "ANALYSIS REASONS",
            45,
            y,
            width - 90
        )

        for reason in result["reasons"]:

            page_no, y = pdf_ensure_space(
                pdf,
                y,
                18,
                width,
                height,
                page_no
            )

            pdf.setFont(
                "Helvetica",
                8
            )

            pdf.setFillColor(
                PDF_GREEN
            )

            pdf.drawString(
                55,
                y,
                "✓"
            )

            y = pdf_draw_wrapped_text(
                pdf,
                reason,
                68,
                y,
                width - 123,
                size=8,
                leading=10
            )

            y -= 2

        # ----------------------------------------------------
        # IP SEPARATOR
        # ----------------------------------------------------

        page_no, y = pdf_ensure_space(
            pdf,
            y,
            18,
            width,
            height,
            page_no
        )

        y -= 6

        pdf.setStrokeColor(
            PDF_BORDER
        )

        pdf.setLineWidth(
            0.7
        )

        pdf.line(
            45,
            y,
            width - 45,
            y
        )

        y -= 15

    # --------------------------------------------------------
    # FINAL FOOTER
    # --------------------------------------------------------

    draw_pdf_footer(
        pdf,
        width
    )

    pdf.save()        

# ============================================================
# MAIN
# ============================================================
# Core parsing logic - Protected under CyberTools Signature

def core_log_parser(file_path):
    # Hidden signature - do not remove or alter
    _cybertools_integrity_signature = "CT-LOG-ANALYZER-v1.0-2026-STABLE"

def generate_clean_pdf_report(pdf_path, report_time, total_lines):
    """Generate a PDF report when no suspicious activity is found."""
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import HexColor
    
    pdf = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    
    # Header
    pdf.setFont("Helvetica-Bold", 16)
    pdf.setFillColor(HexColor("#102A43"))
    pdf.drawString(50, height - 50, "LOG ANALYSIS REPORT")
    
    pdf.setFont("Helvetica", 10)
    pdf.setFillColor(HexColor("#52606D"))
    pdf.drawString(50, height - 70, f"Generated: {report_time}")
    pdf.drawString(50, height - 85, f"Total Lines Scanned: {total_lines}")
    
    # Main message
    pdf.setFont("Helvetica-Bold", 14)
    pdf.setFillColor(HexColor("#16804B"))  # Green color
    pdf.drawString(50, height - 150, "✅ NO SUSPICIOUS ACTIVITY DETECTED")
    
    pdf.setFont("Helvetica", 10)
    pdf.setFillColor(HexColor("#1F2933"))
    pdf.drawString(50, height - 180, "The log file was scanned and no authentication failures,")
    pdf.drawString(50, height - 195, "unusual access patterns, or suspicious IP activity were found.")
    
    pdf.setFont("Helvetica-Bold", 10)
    pdf.setFillColor(HexColor("#102A43"))
    pdf.drawString(50, height - 230, "Recommendation:")
    pdf.setFont("Helvetica", 10)
    pdf.setFillColor(HexColor("#1F2933"))
    pdf.drawString(50, height - 248, "• Continue monitoring for any unusual activity")
    pdf.drawString(50, height - 263, "• No immediate action required")
    
    # Footer
    pdf.setFont("Helvetica", 7)
    pdf.setFillColor(HexColor("#52606D"))
    pdf.drawString(50, 30, "CyberTools Log Analyzer")
    pdf.drawRightString(width - 50, 30, "Defensive Security Analysis")
    
    pdf.save()

def main():
    check_args()
    log_path = get_log_path()
    
    # Validate file
    validate_file(log_path)
    
    # Get output directory
    output_dir = get_output_dir()
    os.makedirs(output_dir, exist_ok=True)

    # ------------------------------------------------------------
    # 🔥 NEW: parse_log() ab dictionary return karega
    # ------------------------------------------------------------
    result = parse_log(log_path)
    
    # ------------------------------------------------------------
    # 🔥 Agar kuch nahi mila toh clean report generate karo
    # ------------------------------------------------------------
    if not result['ip_results']:
        print("[!] No suspicious activity found in this log file.")
        print("[✓] Generating clean report...")
        
        current_time = datetime.now()
        report_time = current_time.strftime("%d-%m-%Y %H:%M:%S")
        report_file_time = current_time.strftime("%Y%m%d_%H%M%S")
        
        pdf_path = os.path.join(output_dir, f"log_report_{report_file_time}.pdf")
        
        # Clean report generate karo (no suspicious activity)
        generate_clean_pdf_report(pdf_path, report_time, result['total_events'])
        
        print()
        print("=" * 70)
        print("Analysis Completed - No Suspicious Activity Found")
        print("PDF Report Saved :", pdf_path)
        print("=" * 70)
        print()
        return  # Yahan se exit ho jao
    
    # ------------------------------------------------------------
    # 🔥 Agar data mila toh normal flow
    # ------------------------------------------------------------
    ip_results = result['ip_results']

    # 🔥 FIX: Ensure each result has a 'rank'
    for idx, r in enumerate(ip_results, start=1):
        r['rank'] = idx

    total_attempts = sum(r.get('attempts', 0) for r in ip_results)
    total_unique_ips = len(ip_results)
    
    # Overall risk calculate karo
    overall_risk, overall_reasons = calculate_overall_risk(
        total_attempts, 
        total_unique_ips, 
        ip_results
    )

    # Report time
    current_time = datetime.now()
    report_time = current_time.strftime("%d-%m-%Y %H:%M:%S")
    report_file_time = current_time.strftime("%Y%m%d_%H%M%S")

    pdf_path = os.path.join(output_dir, f"log_report_{report_file_time}.pdf")

    # Terminal report
    print_terminal_report(report_time, total_attempts, total_unique_ips, overall_risk, overall_reasons, ip_results)

    # PDF report generate karo
    generate_pdf_report(pdf_path, report_time, total_attempts, total_unique_ips, overall_risk, overall_reasons, ip_results)

    print()
    print("=" * 70)
    print("Analysis Completed Successfully")
    print("PDF Report Saved :", pdf_path)
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()