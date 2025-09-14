import xml.etree.ElementTree as element_tree


def read_invoice_data(xml_file_path):
    """
    Reads and extracts key information from the provided XML invoice file.

    Args:
        xml_file_path (str): The path to the XML file.

    Returns:
        dict: A dictionary containing the extracted invoice data, or None if an error occurs.
    """
    try:
        tree = element_tree.parse(xml_file_path)
        root = tree.getroot()

        # Define the namespaces to handle UBL elements correctly
        namespaces = {
            "cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
            "cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            "sts": "dian:gov:co:facturaelectronica:Structures-2-1",
        }

        # --- Extract Invoice Information ---
        invoice_id = root.find("cbc:ID", namespaces).text
        issue_date = root.find("cbc:IssueDate", namespaces).text
        invoice_type_code = root.find("cbc:InvoiceTypeCode", namespaces).text

        # --- Extract Supplier Information ---
        supplier_party = root.find("cac:AccountingSupplierParty", namespaces)
        supplier_name = supplier_party.find(
            "cac:Party/cac:PartyLegalEntity/cbc:RegistrationName", namespaces
        ).text
        supplier_company_id = supplier_party.find(
            "cac:Party/cac:PartyTaxScheme/cbc:CompanyID", namespaces
        ).text

        # --- Extract Customer Information ---
        customer_party = root.find("cac:AccountingCustomerParty", namespaces)
        customer_name = customer_party.find(
            "cac:Party/cac:PartyLegalEntity/cbc:RegistrationName", namespaces
        ).text
        customer_company_id = customer_party.find(
            "cac:Party/cac:PartyTaxScheme/cbc:CompanyID", namespaces
        ).text

        # --- Extract Totals ---
        legal_monetary_total = root.find("cac:LegalMonetaryTotal", namespaces)
        line_extension_amount = legal_monetary_total.find(
            "cbc:LineExtensionAmount", namespaces
        ).text
        tax_inclusive_amount = legal_monetary_total.find(
            "cbc:TaxInclusiveAmount", namespaces
        ).text
        payable_amount = legal_monetary_total.find("cbc:PayableAmount", namespaces).text

        # --- Extract Invoice Lines/Items ---
        invoice_lines = []
        for line in root.findall("cac:InvoiceLine", namespaces):
            item_description = line.find("cac:Item/cbc:Description", namespaces).text
            invoiced_quantity = line.find("cbc:InvoicedQuantity", namespaces).text
            line_extension_amount_line = line.find(
                "cbc:LineExtensionAmount", namespaces
            ).text

            # Check if the line has a price element and get the amount
            price_element = line.find("cac:Price/cbc:PriceAmount", namespaces)
            price_amount = price_element.text if price_element is not None else "N/A"

            invoice_lines.append(
                {
                    "description": item_description,
                    "quantity": invoiced_quantity,
                    "price_per_unit": price_amount,
                    "total_for_line": line_extension_amount_line,
                }
            )

        # --- Consolidate and return the data ---
        invoice_data = {
            "invoice_id": invoice_id,
            "issue_date": issue_date,
            "invoice_type_code": invoice_type_code,
            "supplier": {
                "name": supplier_name,
                "nit": supplier_company_id,
            },
            "customer": {
                "name": customer_name,
                "nit": customer_company_id,
            },
            "totals": {
                "line_extension_amount": line_extension_amount,
                "tax_inclusive_amount": tax_inclusive_amount,
                "payable_amount": payable_amount,
            },
            "invoice_lines": invoice_lines,
        }

        return invoice_data

    except element_tree.ParseError as e:
        print(f"Error parsing the XML file: {e}")
        return None
    except AttributeError as e:
        print(f"Error extracting data. Missing or invalid XML element: {e}")
        return None
