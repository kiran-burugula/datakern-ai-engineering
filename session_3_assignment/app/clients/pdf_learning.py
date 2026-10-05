from PyPDF2 import PdfReader

reader = PdfReader("../../Apex_Financial_Risk_Policy_2026.pdf")

def get_policy_rules(risk_tolerance):

    for page_number, page in enumerate(reader.pages):
        text = page.extract_text() or ""
    
        if risk_tolerance.lower() in text.lower():
            result_dict = {
                "page":page_number + 1,
                "text":text
            }
            return result_dict

    return None

result = get_policy_rules("Conservative")

print(result)