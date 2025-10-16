from flask import Flask, request, jsonify
import requests
import time
import random
import re
from bs4 import BeautifulSoup
from urllib.parse import quote_plus, urlparse
from fake_useragent import UserAgent
from flask_cors import CORS
import concurrent.futures
import threading
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Global lock for thread-safe operations
analysis_lock = threading.Lock()

class AdvancedBINDorkSearchTool:
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
        ]
        self.session = None
        self.search_engines = [
            'google', 'bing', 'yahoo', 'duckduckgo', 
            'brave', 'yandex', 'baidu', 'aol', 'ask'
        ]
    
    def get_session(self):
        if not self.session:
            self.session = requests.Session()
        return self.session
    
    def get_random_agent(self):
        return random.choice(self.user_agents)
    
    def check_protection(self, url):
        """Check if URL has protection like CAPTCHA"""
        try:
            headers = {'User-Agent': self.get_random_agent()}
            res = requests.get(url, headers=headers, timeout=8, allow_redirects=True)
            content = res.text.lower()
            protection_indicators = ['captcha', 'cloudflare', 'security check', 'firewall', 'ddos protection', 'access denied']
            return any(x in content for x in protection_indicators)
        except:
            return False
    
    def search_google(self, query, pages=5):
        """Search using Google with improved parsing"""
        results = []
        for page in range(pages):
            try:
                start = page * 10
                url = f"https://www.google.com/search?q={quote_plus(query)}&start={start}&num=100"
                
                headers = {'User-Agent': self.get_random_agent()}
                response = requests.get(url, headers=headers, timeout=20)
                
                if response.status_code != 200:
                    print(f"Google search returned status {response.status_code}")
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find all search result links
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    if href.startswith('/url?q='):
                        try:
                            link = href.split('/url?q=')[1].split('&')[0]
                            parsed_url = urlparse(link)
                            if parsed_url.netloc and 'google.com' not in parsed_url.netloc:
                                if link not in results:
                                    results.append(link)
                        except:
                            continue
                
                time.sleep(random.uniform(1, 2))
                
            except Exception as e:
                print(f"Google search error: {e}")
                continue
        
        return results
    
    def search_bing(self, query, pages=5):
        """Search using Bing"""
        results = []
        for page in range(1, pages + 1):
            try:
                url = f"https://www.bing.com/search?q={quote_plus(query)}&first={(page-1)*10+1}&count=50"
                
                headers = {'User-Agent': self.get_random_agent()}
                response = requests.get(url, headers=headers, timeout=20)
                
                if response.status_code != 200:
                    print(f"Bing search returned status {response.status_code}")
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find organic results
                for li in soup.find_all('li', class_='b_algo'):
                    a = li.find('a')
                    if a and a.has_attr('href'):
                        href = a['href']
                        if href.startswith('http') and 'bing.com' not in href:
                            if href not in results:
                                results.append(href)
                
                time.sleep(random.uniform(1, 2))
                
            except Exception as e:
                print(f"Bing search error: {e}")
                continue
        
        return results
    
    def search_yahoo(self, query, pages=4):
        """Search using Yahoo"""
        results = []
        for page in range(1, pages + 1):
            try:
                url = f"https://search.yahoo.com/search?p={quote_plus(query)}&b={(page-1)*10+1}"
                
                headers = {'User-Agent': self.get_random_agent()}
                response = requests.get(url, headers=headers, timeout=20)
                
                if response.status_code != 200:
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find search results
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    if href.startswith('http') and 'yahoo.com' not in href:
                        if href not in results:
                            results.append(href)
                
                time.sleep(random.uniform(1, 2))
                
            except Exception as e:
                print(f"Yahoo search error: {e}")
                continue
        
        return results
    
    def search_all_engines(self, query, pages=3, engines=None):
        """Search using multiple search engines"""
        all_results = []
        
        print(f"🔍 Searching for: {query}")
        
        if engines is None:
            engines = ['google', 'bing', 'yahoo']
        
        # Map engine names to methods
        engine_methods = {
            'google': self.search_google,
            'bing': self.search_bing,
            'yahoo': self.search_yahoo
        }
        
        # Search selected engines in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(engines)) as executor:
            futures = {}
            
            for engine in engines:
                if engine in engine_methods:
                    futures[executor.submit(engine_methods[engine], query, pages)] = engine
            
            for future in concurrent.futures.as_completed(futures):
                engine = futures[future]
                try:
                    results = future.result(timeout=30)
                    all_results.extend(results)
                    print(f"✅ {engine} found {len(results)} results")
                except Exception as e:
                    print(f"❌ {engine} search failed: {e}")
        
        # Remove duplicates
        unique_results = list(set(all_results))
        print(f"📊 Total unique results: {len(unique_results)}")
        return unique_results

def check_bin_info(bin_number):
    """Check BIN information using binlist.net API"""
    try:
        api = requests.get(f'https://lookup.binlist.net/{bin_number[:6]}', timeout=10).json()
        
        # Extract information with error handling
        try:
            scheme = api['scheme'].upper()
        except:
            scheme = 'UNKNOWN'
        
        try:
            card_type = api['type'].upper()
        except:
            card_type = 'UNKNOWN'
        
        try:
            brand = api['brand'].upper()
        except:
            brand = 'UNKNOWN'
        
        try:
            bank_name = api['bank']['name'].upper()
        except:
            bank_name = 'UNKNOWN'
        
        try:
            country = api['country']['name']
        except:
            country = 'UNKNOWN'
        
        try:
            bank_url = api['bank']['url']
        except:
            bank_url = 'UNKNOWN'
        
        try:
            bank_phone = api['bank']['phone']
        except:
            bank_phone = 'UNKNOWN'
        
        try:
            country_alpha2 = api['country']['alpha2']
        except:
            country_alpha2 = 'UNKNOWN'
        
        return {
            'bin': bin_number[:6],
            'scheme': scheme,
            'type': card_type,
            'brand': brand,
            'bank': bank_name,
            'country': country,
            'country_code': country_alpha2,
            'bank_url': bank_url,
            'bank_phone': bank_phone,
            'valid': True
        }
    except Exception as e:
        return {
            'bin': bin_number[:6],
            'valid': False,
            'error': str(e)
        }

def advanced_extract_bins_from_text(text, url):
    """Advanced BIN extraction from text with pattern recognition"""
    # More specific BIN patterns
    bin_patterns = [
        r'\b\d{6}\b',  # Exactly 6 digits (BIN)
        r'\b4[0-9]{5}\b',  # Visa BIN (starts with 4)
        r'\b5[1-5][0-9]{4}\b',  # MasterCard BIN (51-55)
        r'\b3[47][0-9]{4}\b',  # American Express BIN
        r'\b3(?:0[0-5]|[68][0-9])[0-9]{3}\b',  # Diners Club BIN
        r'\b6(?:011|5[0-9]{2})[0-9]{3}\b',  # Discover BIN
        r'\b(?:2131|1800|35\d{3})\b',  # JCB BIN
    ]
    
    # Card number patterns (extract first 6 digits)
    card_patterns = [
        r'\b4[0-9]{12,15}\b',  # Visa cards (16 digits)
        r'\b5[1-5][0-9]{14}\b',  # MasterCard (16 digits)
        r'\b3[47][0-9]{13}\b',  # American Express (15 digits)
        r'\b3(?:0[0-5]|[68][0-9])[0-9]{11,12}\b',  # Diners Club (14-16)
        r'\b6(?:011|5[0-9]{2})[0-9]{12}\b',  # Discover (16 digits)
        r'\b(?:2131|1800|35\d{3})\d{11}\b',  # JCB (15 digits)
    ]
    
    bins_found = set()
    
    # Extract direct BINs
    for pattern in bin_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if len(match) == 6:
                bins_found.add(match)
    
    # Extract BINs from card numbers
    for pattern in card_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if len(match) >= 6:
                bin_num = match[:6]
                bins_found.add(bin_num)
    
    # Look for BINs in specific contexts (tables, lists, etc.)
    context_patterns = [
        r'BIN[\s:]*(\d{6})',
        r'bin[\s:]*(\d{6})',
        r'Bank[\s\S]{0,200}?(\d{6})',
        r'Card[\s\S]{0,200}?(\d{6})',
        r'\d{6}[\s\S]{0,100}?(?:Visa|MasterCard|American Express|Discover)',
        r'(?:Visa|MasterCard|American Express|Discover)[\s\S]{0,100}?(\d{6})'
    ]
    
    for pattern in context_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if match.isdigit() and len(match) == 6:
                bins_found.add(match)
    
    return list(bins_found)

def deep_bin_analysis(url):
    """Deep analysis of URL for BIN extraction"""
    try:
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        response = requests.get(url, headers=headers, timeout=20, allow_redirects=True)
        
        if response.status_code != 200:
            return None
            
        text = response.text
        soup = BeautifulSoup(text, 'html.parser')
        
        # Remove scripts and styles
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get clean text
        clean_text = soup.get_text()
        
        # Extract BINs from main text
        bins_found = advanced_extract_bins_from_text(clean_text, url)
        
        # Also check specific HTML elements that might contain BINs
        html_specific_locations = [
            soup.find_all('td'),
            soup.find_all('span'),
            soup.find_all('div', class_=re.compile(r'bin|card|number', re.I)),
            soup.find_all('pre'),
            soup.find_all('code')
        ]
        
        for elements in html_specific_locations:
            for element in elements:
                element_text = element.get_text()
                element_bins = advanced_extract_bins_from_text(element_text, url)
                bins_found.extend(element_bins)
        
        # Remove duplicates
        bins_found = list(set(bins_found))
        
        if not bins_found:
            return None
        
        # Check BIN information for each found BIN
        valid_bins = []
        for bin_num in bins_found:
            bin_info = check_bin_info(bin_num)
            if bin_info['valid']:
                valid_bins.append(bin_info)
            time.sleep(0.5)  # Rate limiting
        
        return {
            'url': url,
            'bins_found': len(bins_found),
            'valid_bins': valid_bins,
            'total_valid_bins': len(valid_bins),
            'deep_analysis': True
        }
        
    except Exception as e:
        print(f"❌ Error in deep analysis of {url}: {e}")
        return None

def generate_bin_dorks(bank_name=None, country=None, card_type=None):
    """Generate precise BIN search dorks"""
    
    base_dorks = [
        # Direct BIN list dorks
        '"BIN list" "download"',
        '"BIN database" "csv"',
        '"card BIN numbers" "list"',
        '"bank identification number" "database"',
        '"BIN ranges" "excel"',
        '"credit card BIN" "download"',
        
        # File-specific dorks
        '"BIN" "filetype:csv"',
        '"BIN list" "filetype:xlsx"',
        '"BIN database" "filetype:txt"',
        '"card numbers" "filetype:pdf"',
        
        # Forum and community dorks
        '"BIN list" "forum"',
        '"card BIN" "pastebin"',
        '"BIN database" "github"',
        '"credit card BIN" "reddit"',
        
        # Technical dorks
        '"BIN lookup" "API"',
        '"bank BIN" "JSON"',
        '"card scheme" "database"',
        
        # Comprehensive dorks
        '"BIN list" "Visa MasterCard American Express"',
        '"complete BIN database"',
        '"updated BIN list"',
        '"fresh BIN numbers"',
    ]
    
    # Bank-specific dorks
    if bank_name:
        bank_dorks = [
            f'"{bank_name}" "BIN list"',
            f'"{bank_name}" "card BIN"',
            f'"{bank_name}" "bank identification number"',
            f'BIN "{bank_name}" "database"',
            f'"{bank_name}" "credit card BIN"',
            f'"{bank_name}" BIN ranges',
            f'bin list "{bank_name}" bank',
            f'bin "{bank_name}" bank',
            f'"{bank_name}" bin list',
        ]
        base_dorks = bank_dorks + base_dorks
    
    # Country-specific dorks
    if country:
        country_dorks = [
            f'"{country}" "BIN list"',
            f'"{country}" "card BIN"',
            f'BIN "{country}" "banks"',
        ]
        base_dorks = country_dorks + base_dorks
    
    # Card type specific dorks
    if card_type:
        type_dorks = [
            f'"{card_type}" "BIN list"',
            f'"{card_type}" "card BIN"',
        ]
        base_dorks = type_dorks + base_dorks
    
    return base_dorks

# BIN Generation Methods
def activation_method(card_number):
    """Method 1: Activation Extraction - Replace last 6 digits with X"""
    if len(card_number) >= 16:
        return card_number[:10] + 'x' * 6
    return None

def similarity_method(card1, card2):
    """Method 2: Similarity Extraction - Compare two cards and mark differences with X"""
    if len(card1) != len(card2) or len(card1) < 16:
        return None
    
    bin_part = card1[:6]
    remaining1 = card1[6:]
    remaining2 = card2[6:]
    
    result = bin_part
    for i in range(len(remaining1)):
        if remaining1[i] == remaining2[i]:
            result += remaining1[i]
        else:
            result += 'x'
    
    return result

def pattern_method(cards):
    """Method 3: Pattern Extraction - Find repeating patterns in multiple cards"""
    if len(cards) < 2:
        return None
    
    bin_part = cards[0][:6]
    patterns = []
    
    for i in range(6, 16):
        digits = [card[i] for card in cards if len(card) > i]
        if len(set(digits)) == 1:  # All same digit
            patterns.append(digits[0])
        else:
            patterns.append('x')
    
    return bin_part + ''.join(patterns)

def sofia_method(card1, card2):
    """Method 4: Sofia Method - Mathematical processing of middle digits"""
    if len(card1) != len(card2) or len(card1) < 16:
        return None
    
    # Take digits from middle of third group (positions 8-9)
    try:
        mid1_1 = int(card1[8])
        mid1_2 = int(card1[9])
        mid2_1 = int(card2[8])
        mid2_2 = int(card2[9])
        
        # Sum and process
        sum1 = mid1_1 + mid2_1
        sum2 = mid1_2 + mid2_2
        
        result1 = int((sum1 / 2) * 5)
        result2 = int((sum2 / 2) * 5)
        
        final = result1 + result2
        
        return card1[:10] + str(final).zfill(2) + 'x' * 4
    except:
        return None

def logical_indentation_method(card):
    """Method 5: Logical Indentation - Group processing with pattern recognition"""
    if len(card) < 16:
        return None
    
    working_part = '0' + card[6:]  # Add leading zero
    groups = []
    
    # Split into groups of 3-4-3
    if len(working_part) >= 10:
        groups = [working_part[:3], working_part[3:7], working_part[7:10]]
    else:
        return None
    
    result = card[:6]
    for group in groups:
        if len(group) == 3:
            result += group[0] + 'x' + group[2]
        elif len(group) == 4:
            result += group[0] + 'xx' + group[3]
        else:
            result += group
    
    return result

def material_dinverter_method(card1, card2):
    """Method 6: Material DInVerter - Complex multiplication and processing"""
    if len(card1) != len(card2) or len(card1) < 16:
        return None
    
    try:
        # Take parts from position 8-11
        part1 = card1[8:12]
        part2 = card2[8:12]
        
        multiplied = ''
        for i in range(min(len(part1), len(part2))):
            product = int(part1[i]) * int(part2[i])
            multiplied += str(product)
        
        # Take first 8 digits
        if len(multiplied) > 8:
            multiplied = multiplied[:8]
        elif len(multiplied) < 8:
            multiplied = multiplied.ljust(8, '0')
        
        result = card1[:8] + multiplied + card1[16:]
        return result
    except:
        return None

def generate_bin_from_methods(cards_data, method="all"):
    """Generate BIN patterns using all methods and validate them"""
    valid_patterns = []
    
    if method == "all" or method == "activation":
        # Method 1: Activation
        if len(cards_data) >= 1:
            pattern1 = activation_method(cards_data[0])
            if pattern1:
                bin_info = check_bin_info(pattern1)
                if bin_info['valid']:
                    valid_patterns.append({
                        'method': 'Activation Method',
                        'pattern': pattern1,
                        'info': bin_info
                    })
    
    if method == "all" or method == "similarity":
        # Method 2: Similarity
        if len(cards_data) >= 2:
            pattern2 = similarity_method(cards_data[0], cards_data[1])
            if pattern2:
                bin_info = check_bin_info(pattern2)
                if bin_info['valid']:
                    valid_patterns.append({
                        'method': 'Similarity Method', 
                        'pattern': pattern2,
                        'info': bin_info
                    })
    
    if method == "all" or method == "pattern":
        # Method 3: Pattern
        if len(cards_data) >= 2:
            pattern3 = pattern_method(cards_data[:3])
            if pattern3:
                bin_info = check_bin_info(pattern3)
                if bin_info['valid']:
                    valid_patterns.append({
                        'method': 'Pattern Method',
                        'pattern': pattern3,
                        'info': bin_info
                    })
    
    if method == "all" or method == "sofia":
        # Method 4: Sofia
        if len(cards_data) >= 2:
            pattern4 = sofia_method(cards_data[0], cards_data[1])
            if pattern4:
                bin_info = check_bin_info(pattern4)
                if bin_info['valid']:
                    valid_patterns.append({
                        'method': 'Sofia Method',
                        'pattern': pattern4,
                        'info': bin_info
                    })
    
    if method == "all" or method == "logical":
        # Method 5: Logical Indentation
        if len(cards_data) >= 1:
            pattern5 = logical_indentation_method(cards_data[0])
            if pattern5:
                bin_info = check_bin_info(pattern5)
                if bin_info['valid']:
                    valid_patterns.append({
                        'method': 'Logical Indentation Method',
                        'pattern': pattern5,
                        'info': bin_info
                    })
    
    if method == "all" or method == "material":
        # Method 6: Material DInVerter
        if len(cards_data) >= 2:
            pattern6 = material_dinverter_method(cards_data[0], cards_data[1])
            if pattern6:
                bin_info = check_bin_info(pattern6)
                if bin_info['valid']:
                    valid_patterns.append({
                        'method': 'Material DInVerter Method',
                        'pattern': pattern6,
                        'info': bin_info
                    })
    
    return valid_patterns

def send_telegram_message_sync(bot_token, chat_id, message):
    """Send message to Telegram bot synchronously"""
    try:
        import telegram
        bot = telegram.Bot(token=bot_token)
        bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')
        return True
    except Exception as e:
        print(f"❌ Telegram error: {e}")
        return False

# API Routes
@app.route('/bin/check', methods=['GET'])
def check_bin():
    """API endpoint to check a single BIN"""
    bin_number = request.args.get('bin')
    
    if not bin_number or len(bin_number) < 6:
        return jsonify({
            'error': 'Valid BIN number (6+ digits) is required',
            'api_by': '@R_O_P_D'
        }), 400
    
    try:
        bin_info = check_bin_info(bin_number)
        return jsonify({
            'result': bin_info,
            'api_by': '@R_O_P_D'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Unexpected error: {str(e)}',
            'api_by': '@R_O_P_D'
        }), 500

@app.route('/bin/search', methods=['GET'])
def search_bins():
    """Advanced BIN search endpoint with precise dorks"""
    try:
        # Get query parameters
        pages = int(request.args.get('pages', 3))
        max_results = int(request.args.get('max_results', 50))
        min_bins = int(request.args.get('min_bins', 10))
        bank_name = request.args.get('bank_name')
        country = request.args.get('country')
        card_type = request.args.get('card_type')
        search_engines = request.args.get('search_engines')
        custom_query = request.args.get('custom_query')
        bot_token = request.args.get('bot_token')
        chat_id = request.args.get('chat_id')
        
        # Parse search engines
        engines_list = None
        if search_engines:
            engines_list = [engine.strip().lower() for engine in search_engines.split(',')]
        
        # Generate precise dorks
        bin_dorks = generate_bin_dorks(bank_name, country, card_type)
        
        # Add custom query if provided
        if custom_query:
            bin_dorks.insert(0, custom_query)
        
        tool = AdvancedBINDorkSearchTool()
        all_valid_results = []
        
        print(f"🎯 Using {len(bin_dorks)} precise dorks for search")
        
        # Search with multiple precise dorks
        for i, dork in enumerate(bin_dorks):
            if len(all_valid_results) >= max_results * 2:
                break
                
            print(f"🔍 Dork {i+1}/{len(bin_dorks)}: {dork}")
            results = tool.search_all_engines(dork, min(pages, 2), engines_list)
            all_valid_results.extend(results)
            
            # Be respectful with delays
            time.sleep(random.uniform(2, 4))
        
        # Remove duplicates
        all_valid_results = list(set(all_valid_results))
        print(f"📊 Found {len(all_valid_results)} unique URLs to analyze")
        
        # Deep analyze URLs for BINs with threading
        analyzed_sources = []
        all_valid_bins = []
        
        def deep_analyze_url(url):
            result = deep_bin_analysis(url)
            if result and result['valid_bins']:
                # Apply additional filters
                filtered_bins = []
                for bin_info in result['valid_bins']:
                    if bank_name and bank_name.upper() not in bin_info['bank']:
                        continue
                    if country and country.upper() not in bin_info['country'].upper():
                        continue
                    if card_type and card_type.upper() not in bin_info['type']:
                        continue
                    filtered_bins.append(bin_info)
                
                if filtered_bins:
                    result['valid_bins'] = filtered_bins
                    result['total_valid_bins'] = len(filtered_bins)
                    return result
            return None
        
        # Use threading for faster deep analysis
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {executor.submit(deep_analyze_url, url): url for url in all_valid_results[:max_results]}
            
            for future in concurrent.futures.as_completed(future_to_url):
                result = future.result()
                if result:
                    analyzed_sources.append(result)
                    all_valid_bins.extend(result['valid_bins'])
                    
                    print(f"✅ Found {result['total_valid_bins']} valid BINs from {result['url']}")
                    
                    # Stop if we have enough BINs
                    if len(all_valid_bins) >= min_bins * 2:
                        break
        
        # Remove duplicate BINs
        unique_bins = []
        seen_bins = set()
        for bin_info in all_valid_bins:
            if bin_info['bin'] not in seen_bins:
                unique_bins.append(bin_info)
                seen_bins.add(bin_info['bin'])
        
        # Take requested number of BINs
        final_bins = unique_bins[:min_bins]
        
        # Prepare response
        response_data = {
            'dorks_used': len(bin_dorks),
            'sources_analyzed': len(analyzed_sources),
            'total_bins_found': len(unique_bins),
            'bins_returned': len(final_bins),
            'bins': final_bins,
            'api_by': '@R_O_P_D',
            'message': 'Advanced BIN search completed successfully',
            'search_parameters': {
                'pages': pages,
                'max_results': max_results,
                'min_bins': min_bins,
                'bank_name': bank_name,
                'country': country,
                'card_type': card_type,
                'search_engines': engines_list or 'google,bing,yahoo'
            },
            'deep_analysis': True,
            'timestamp': datetime.now().isoformat()
        }
        
        # Send to Telegram if token and chat_id provided
        if bot_token and chat_id and final_bins:
            message = f"<b>🔍 Advanced BIN Search Results</b>\n\n"
            message += f"<b>BINs Found:</b> {len(final_bins)}\n"
            message += f"<b>Bank:</b> {bank_name or 'Any'}\n"
            message += f"<b>Country:</b> {country or 'Any'}\n"
            message += f"<b>Card Type:</b> {card_type or 'Any'}\n"
            message += f"<b>Deep Analysis:</b> Yes\n"
            message += f"<b>Timestamp:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            for i, bin_info in enumerate(final_bins[:8]):  # Send first 8 BINs
                message += f"<b>BIN {i+1}:</b> {bin_info['bin']}\n"
                message += f"<b>Scheme:</b> {bin_info['scheme']}\n"
                message += f"<b>Type:</b> {bin_info['type']}\n"
                message += f"<b>Bank:</b> {bin_info['bank']}\n"
                message += f"<b>Country:</b> {bin_info['country']}\n"
                message += f"<b>Brand:</b> {bin_info['brand']}\n\n"
            
            if len(final_bins) > 8:
                message += f"<i>... and {len(final_bins) - 8} more BINs</i>\n\n"
            
            message += f"<b>API by:</b> @R_O_P_D"
            
            # Send message in a separate thread
            threading.Thread(target=send_telegram_message_sync, args=(bot_token, chat_id, message)).start()
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'error': f'Unexpected error: {str(e)}',
            'api_by': '@R_O_P_D'
        }), 500

@app.route('/bin/dorks', methods=['GET'])
def get_bin_dorks():
    """Get generated BIN search dorks"""
    bank_name = request.args.get('bank_name')
    country = request.args.get('country')
    card_type = request.args.get('card_type')
    
    dorks = generate_bin_dorks(bank_name, country, card_type)
    
    return jsonify({
        'dorks': dorks,
        'count': len(dorks),
        'parameters': {
            'bank_name': bank_name,
            'country': country,
            'card_type': card_type
        },
        'api_by': '@R_O_P_D'
    })

@app.route('/bin/generate', methods=['POST'])
def generate_bin_patterns():
    """Generate BIN patterns from card numbers using multiple methods"""
    try:
        data = request.get_json()
        
        if not data or 'cards' not in data:
            return jsonify({
                'error': 'Card numbers are required in JSON format',
                'api_by': '@R_O_P_D'
            }), 400
        
        cards = data['cards']
        method = data.get('method', 'all')
        
        if not isinstance(cards, list) or len(cards) == 0:
            return jsonify({
                'error': 'At least one card number is required',
                'api_by': '@R_O_P_D'
            }), 400
        
        # Validate card numbers
        for card in cards:
            if not re.match(r'^\d{13,19}$', str(card)):
                return jsonify({
                    'error': f'Invalid card number: {card}. Must be 13-19 digits',
                    'api_by': '@R_O_P_D'
                }), 400
        
        # Check method requirements
        if method in ['similarity', 'sofia', 'material'] and len(cards) < 2:
            return jsonify({
                'error': f'{method} method requires at least 2 card numbers',
                'api_by': '@R_O_P_D'
            }), 400
        
        if method == 'pattern' and len(cards) < 2:
            return jsonify({
                'error': 'Pattern method requires at least 2 card numbers',
                'api_by': '@R_O_P_D'
            }), 400
        
        # Generate BIN patterns using all methods
        generated_patterns = generate_bin_from_methods(cards, method)
        
        response_data = {
            'input_cards': len(cards),
            'generated_patterns': len(generated_patterns),
            'patterns': generated_patterns,
            'method_used': method,
            'api_by': '@R_O_P_D',
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'error': f'Unexpected error: {str(e)}',
            'api_by': '@R_O_P_D'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'OK',
        'message': 'Advanced BIN Analysis API is running',
        'api_by': '@R_O_P_D',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/methods', methods=['GET'])
def list_methods():
    """List all available BIN generation methods"""
    methods = [
        {
            'name': 'Activation Method',
            'description': 'Replaces last 6 digits with X',
            'required_cards': 1,
            'endpoint': 'activation'
        },
        {
            'name': 'Similarity Method', 
            'description': 'Compares two cards and marks differences with X',
            'required_cards': 2,
            'endpoint': 'similarity'
        },
        {
            'name': 'Pattern Method',
            'description': 'Finds repeating patterns in multiple cards',
            'required_cards': 2,
            'endpoint': 'pattern'
        },
        {
            'name': 'Sofia Method',
            'description': 'Mathematical processing of middle digits',
            'required_cards': 2,
            'endpoint': 'sofia'
        },
        {
            'name': 'Logical Indentation Method',
            'description': 'Groups digits and processes logically',
            'required_cards': 1,
            'endpoint': 'logical'
        },
        {
            'name': 'Material DInVerter Method',
            'description': 'Complex multiplication and processing',
            'required_cards': 2,
            'endpoint': 'material'
        }
    ]
    
    return jsonify({
        'methods': methods,
        'total_methods': len(methods),
        'api_by': '@R_O_P_D'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
