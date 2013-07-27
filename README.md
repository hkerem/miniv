Requirements
================
Python 2.7
Python modules: web.py (0.34), pysqlite2 (2.6.3), requests (0.8.2), nose (1.1.2), json, cmd (default Ubuntu 12.04 packages)

Commands
================
Miniv is a client/server application.

To run miniv server: 

    # ./run_server.sh

To run miniv client:

    # ./run_client.sh
    
To cleanup miniv server state: 

    # ./cleanup_server.sh

Example
================

    shell-1# ./run_server.sh

and

    shell-2# ./run_client.sh
    Mini-V Application Interactive CLI Terminal
    > user Thomas
    -- Created user successfully
    > user Lisa
    -- Created user successfully
    > user Quincy
    -- Created user successfully
    > add Thomas 4111111111111111
    -- Added credit card to user successfully
    > add Lisa 5454545454545454
    -- Added credit card to user successfully
    > add Quincy 1234567890123456
    ERROR: This card is invalid.
    > pay Thomas Lisa $10.25 burritos
    -- Completed payment successfully
    > pay Thomas Quincy $10.00 you’re awesome
    -- Completed payment successfully
    > pay Lisa Quincy $5.00 pot-luck supplies
    -- Completed payment successfully
    > pay Quincy Thomas $2.00 a subway card
    ERROR: This user does not have a credit card.
    > add Quincy 5454545454545454
    ERROR: That card has already been added by another user, reported for fraud!
    > add Quincy 5555555555554444
    -- Added credit card to user successfully
    > pay Quincy Thomas $14.50 a redbull vodka
    -- Completed payment successfully
    > feed Quincy
    -- Thomas paid you $10 for you’re awesome
    -- Lisa paid you $5 for pot-luck supplies
    -- You paid Thomas $14.5 for a redbull vodka
    > balance Quincy
    -- $15
    > feed Thomas
    -- You paid Lisa $10.25 for burritos
    -- You paid Quincy $10 for you’re awesome
    -- Quincy paid you $14.5 for a redbull vodka
    > feed Lisa
    -- Thomas paid you $10.25 for burritos
    -- You paid Quincy $5 for pot-luck supplies
    > 
    



