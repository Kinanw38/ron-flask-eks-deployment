from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="he" dir="ltr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ron's DevOps Mission</title>
        <style>
            :root {
                --bg: #0b0f1a;
                --card: #161b2b;
                --text: #f8fafc;
                --text-dim: #94a3b8;
                /* Brand Colors */
                --terraform: #844fba;
                --aws: #ff9900;
                --docker: #2496ed;
                --eks: #ffc107;
            }
            body {
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
                background-color: var(--bg);
                color: var(--text);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .card {
                background-color: var(--card);
                padding: 3rem;
                border-radius: 24px;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
                text-align: center;
                width: 90%;
                max-width: 480px;
                border: 1px solid rgba(255, 255, 255, 0.05);
                position: relative;
            }
            h1 {
                font-size: 2.4rem;
                margin-bottom: 1rem;
                font-weight: 800;
                letter-spacing: -1px;
            }
            .description {
                color: var(--text-dim);
                line-height: 1.8;
                font-size: 1.15rem;
                margin-bottom: 2.5rem;
            }
            /* Styling for Brand Highlights */
            .tf-color { color: var(--terraform); font-weight: 700; }
            .eks-color { color: var(--eks); font-weight: 700; }
            .docker-color { color: var(--docker); font-weight: 700; }

            .footer {
                border-top: 1px solid rgba(255, 255, 255, 0.08);
                padding-top: 1.5rem;
            }
            .dev-name {
                font-size: 1rem;
                margin-bottom: 8px;
            }
            .hebrew-text {
                font-size: 0.9rem;
                color: var(--text-dim);
                direction: rtl;
                opacity: 0.8;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Mission Complete</h1>
            <p class="description">
                Infrastructure provisioned by <span class="tf-color">Terraform</span><br>
                Managed on <span class="eks-color">AWS EKS</span> Cluster<br>
                Deployed with <span class="docker-color">Docker</span> Containers
            </p>
            <div class="footer">
                <div class="dev-name">Developed by <strong>Ron</strong></div>
                <div class="hebrew-text">התשתית הוקמה בהצלחה ומוכנה לעבודה</div>
            </div>
        </div>
    </body>
    </html>
    """


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)