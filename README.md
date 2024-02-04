# Awesome-Task-Exchange-System
The top management of UberPopug Inc was faced with the problem of employee productivity. To increase productivity, it was decided to throw out the current task tracker and write a special Awesome Task Exchange System (aTES), which should increase employee productivity by an indefinite percentage.

**Business domain**

The main goal of the new aTES system will be to increase employee productivity by an indefinite percentage. The service will allow you to innovatively assign a random employee to each task.

**Sub-domains**
1. Performing tasks
2. Selection of parrots for tasks
3. Increasing the motivation of top managers

| Subdomain view | Competitive Advantage | Difficulty | Variability | Implementation options | Interest problems | Intended type of subdomain |
| --- | --- | --- | --- | --- | --- | --- |
| Executing tasks | no | high | frequent | in-house development | low | generic |
| Choose parrots for tasks | yes | high | frequent | in-house development | high | core |
| Increasing motivation of top managers | no | low | rare | inhouse by weak teams | low | supporting |

After analyzing the business requirements:

1. Event Storming was created
2. Types of subdomains and bounded contexts are highlighted
3. Certain architectural characteristics for each bounded context based on the assumption that our system will be a start-up and financial compliance for contexts that work with money and transactions
4. Instabilities are calculated and services are determined

**Services:**
1. Selection of parrots for tasks
2. Tasks execution
3. Parrots Accounting
4. Managers Accounting

More detailed information with ES, Services and Model Data in Miro - https://miro.com/app/board/uXjVNNALqIc=/

**Service definition context**

The “Selection of parrots for tasks” service will live separately, since it is a core subdomain, it is expected that it will be the most complex, change and be released frequently, and perhaps in the future the business will want to sell it on the market as a separate product.

A service with two contexts “Creating and evaluating tasks” and “Analytics” is also included in a separate service due to the general architectural characteristics.

We will also make the “Parrot Accounting” and “Manager Accounting” services separate, since they have a fin compliance nature (a separate database and strong changes in the business logic of payments are possible, for example, connecting some benefits, coupons, etc.)
