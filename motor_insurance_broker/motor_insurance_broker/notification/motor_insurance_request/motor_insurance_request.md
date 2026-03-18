<h3>Welcome to Our Website</h3>

<p>Hello {{ doc.lead_name or doc.contact_name or doc.name }},</p>

<p>Thank you for showing interest in our services. We have received your lead request.</p>

<p>For further processing, please reply with the message <strong>"Create Quotation"</strong> and our team will prepare a tailored quotation for you.</p>

<h4>Lead Details</h4>

<ul>
<li>Company: {{ doc.company_name or 'N/A' }}</li>
<li>Email: {{ doc.email_id or 'N/A' }}</li>
<li>Status: {{ doc.status }}</li>
</ul>

<p>Best regards,<br>
{{ doc.company or 'Your Company' }}</p>
