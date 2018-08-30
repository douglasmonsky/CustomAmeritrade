sample_orders = [
      {
        "session": "NORMAL",
        "duration": "DAY",
        "orderType": "LIMIT",
        "complexOrderStrategyType": "NONE",
        "quantity": "500",
        "filledQuantity": "343",
        "remainingQuantity": "0",
        "requestedDestination": "AUTO",
        "destinationLinkName": "CDRG",
        "price": "32.7",
        "orderLegCollection": [
          {
            "orderLegType": "EQUITY",
            "legId": "1",
            "instrument": {
              "assetType": "EQUITY",
              "cusip": "707569109",
              "symbol": "PENN"
            },
            "instruction": "BUY",
            "positionEffect": "OPENING",
            "quantity": "500"
          }
        ],
        "orderStrategyType": "SINGLE",
        "orderId": "370336378",
        "cancelable": "false",
        "editable": "false",
        "status": "CANCELED",
        "enteredTime": "2018-08-17T14:55:51+0000",
        "closeTime": "2018-08-17T15:08:39+0000",
        "tag": "WEB_GRID_SNAP",
        "accountId": "425567337",
        "orderActivityCollection": [
          {
            "activityType": "EXECUTION",
            "executionType": "FILL",
            "quantity": "43",
            "orderRemainingQuantity": "457",
            "executionLegs": [
              {
                "legId": "1",
                "quantity": "43",
                "mismarkedQuantity": "0",
                "price": "32.6999",
                "time": "2018-08-17T14:55:51+0000"
              }
            ]
          },
          {
            "activityType": "EXECUTION",
            "executionType": "FILL",
            "quantity": "100",
            "orderRemainingQuantity": "357",
            "executionLegs": [
              {
                "legId": "1",
                "quantity": "100",
                "mismarkedQuantity": "0",
                "price": "32.6999",
                "time": "2018-08-17T14:55:51+0000"
              }
            ]
          },
          {
            "activityType": "EXECUTION",
            "executionType": "FILL",
            "quantity": "100",
            "orderRemainingQuantity": "257",
            "executionLegs": [
              {
                "legId": "1",
                "quantity": "100",
                "mismarkedQuantity": "0",
                "price": "32.6999",
                "time": "2018-08-17T14:55:51+0000"
              }
            ]
          },
          {
            "activityType": "EXECUTION",
            "executionType": "FILL",
            "quantity": "100",
            "orderRemainingQuantity": "157",
            "executionLegs": [
              {
                "legId": "1",
                "quantity": "100",
                "mismarkedQuantity": "0",
                "price": "32.6999",
                "time": "2018-08-17T14:55:51+0000"
              }
            ]
          }
        ]
      },
      {
        "session": "NORMAL",
        "duration": "DAY",
        "orderType": "LIMIT",
        "complexOrderStrategyType": "NONE",
        "quantity": "25",
        "filledQuantity": "25",
        "remainingQuantity": "0",
        "requestedDestination": "AUTO",
        "destinationLinkName": "CDRG",
        "price": "124.94",
        "orderLegCollection": [
          {
            "orderLegType": "EQUITY",
            "legId": "1",
            "instrument": {
              "assetType": "EQUITY",
              "cusip": "874054109",
              "symbol": "TTWO"
            },
            "instruction": "SELL",
            "positionEffect": "CLOSING",
            "quantity": "25"
          }
        ],
        "orderStrategyType": "SINGLE",
        "orderId": "370336366",
        "cancelable": "false",
        "editable": "false",
        "status": "FILLED",
        "enteredTime": "2018-08-17T14:53:42+0000",
        "closeTime": "2018-08-17T14:53:43+0000",
        "tag": "WEB_GRID_SNAP",
        "accountId": "425567337",
        "orderActivityCollection": [
          {
            "activityType": "EXECUTION",
            "executionType": "FILL",
            "quantity": "25",
            "orderRemainingQuantity": "0",
            "executionLegs": [
              {
                "legId": "1",
                "quantity": "25",
                "mismarkedQuantity": "0",
                "price": "124.94",
                "time": "2018-08-17T14:53:43+0000"
              }
            ]
          }
        ]
      }
    ]

sample_orders2 = [
  {
    'session': 'NORMAL',
   'duration': 'DAY',
   'orderType': 'MARKET',
   'complexOrderStrategyType': 'NONE',
   'quantity': 500.0, 'filledQuantity': 500.0,
   'remainingQuantity': 0.0,
   'requestedDestination': 'AUTO',
   'destinationLinkName': 'ETMM',
   'orderLegCollection': [
        {
          'orderLegType': 'EQUITY',
          'legId': 1,
          'instrument':
            {'assetType': 'EQUITY',
             'cusip': '77543R102',
             'symbol': 'ROKU'},
             'instruction': 'SELL',
             'positionEffect': 'CLOSING',
             'quantity': 500.0}],
    'orderStrategyType': 'SINGLE',
    'orderId': 371685592,
    'cancelable': False,
    'editable': False,
    'status': 'FILLED',
    'enteredTime': '2018-08-20T15:44:17+0000',
    'closeTime': '2018-08-20T15:44:17+0000',
    'tag': 'WEB_GRID_SNAP', 'accountId': 425567337,
    'orderActivityCollection': [
        {'activityType': 'EXECUTION',
         'executionType': 'FILL',
         'quantity': 500.0,
         'orderRemainingQuantity': 0.0,
         'executionLegs': [
           {'legId': 1,
            'quantity': 500.0,
            'mismarkedQuantity': 0.0,
            'price': 56.9331,
            'time': '2018-08-20T15:44:17+0000'}
            ]
         }
      ]
    }
  ]


sample_orders3 = [{'session': 'NORMAL', 'duration': 'DAY', 'orderType': 'MARKET', 'complexOrderStrategyType': 'NONE', 'quantity': 500.0, 'filledQuantity': 500.0, 'remainingQuantity': 0.0, 'requestedDestination': 'AUTO', 'destinationLinkName': 'CDRG', 'orderLegCollection': [{'orderLegType': 'EQUITY', 'legId': 1, 'instrument': {'assetType': 'EQUITY', 'cusip': '77543R102', 'symbol': 'ROKU'}, 'instruction': 'BUY', 'positionEffect': 'OPENING', 'quantity': 500.0}], 'orderStrategyType': 'SINGLE', 'orderId': 378977879, 'cancelable': False, 'editable': False, 'status': 'FILLED', 'enteredTime': '2018-08-29T16:07:14+0000', 'closeTime': '2018-08-29T16:07:14+0000', 'tag': 'WEB_GRID_SNAP', 'accountId': 425567337, 'orderActivityCollection': [{'activityType': 'EXECUTION', 'executionType': 'FILL', 'quantity': 500.0, 'orderRemainingQuantity': 0.0, 'executionLegs': [{'legId': 1, 'quantity': 500.0, 'mismarkedQuantity': 0.0, 'price': 60.2607, 'time': '2018-08-29T16:07:14+0000'}]}]}, {'session': 'NORMAL', 'duration': 'DAY', 'orderType': 'MARKET', 'complexOrderStrategyType': 'NONE', 'quantity': 500.0, 'filledQuantity': 500.0, 'remainingQuantity': 0.0, 'requestedDestination': 'AUTO', 'destinationLinkName': 'CDRG', 'orderLegCollection': [{'orderLegType': 'EQUITY', 'legId': 1, 'instrument': {'assetType': 'EQUITY', 'cusip': '77543R102', 'symbol': 'ROKU'}, 'instruction': 'SELL', 'positionEffect': 'CLOSING', 'quantity': 500.0}], 'orderStrategyType': 'SINGLE', 'orderId': 378977810, 'cancelable': False, 'editable': False, 'status': 'FILLED', 'enteredTime': '2018-08-29T15:45:07+0000', 'closeTime': '2018-08-29T15:45:07+0000', 'tag': 'WEB_GRID_SNAP', 'accountId': 425567337, 'orderActivityCollection': [{'activityType': 'EXECUTION', 'executionType': 'FILL', 'quantity': 200.0, 'orderRemainingQuantity': 300.0, 'executionLegs': [{'legId': 1, 'quantity': 200.0, 'mismarkedQuantity': 0.0, 'price': 61.37, 'time': '2018-08-29T15:45:07+0000'}]}, {'activityType': 'EXECUTION', 'executionType': 'FILL', 'quantity': 100.0, 'orderRemainingQuantity': 200.0, 'executionLegs': [{'legId': 1, 'quantity': 100.0, 'mismarkedQuantity': 0.0, 'price': 61.37, 'time': '2018-08-29T15:45:07+0000'}]}, {'activityType': 'EXECUTION', 'executionType': 'FILL', 'quantity': 200.0, 'orderRemainingQuantity': 0.0, 'executionLegs': [{'legId': 1, 'quantity': 200.0, 'mismarkedQuantity': 0.0, 'price': 61.37, 'time': '2018-08-29T15:45:07+0000'}]}]}, {'session': 'NORMAL', 'duration': 'DAY', 'orderType': 'LIMIT', 'complexOrderStrategyType': 'NONE', 'quantity': 500.0, 'filledQuantity': 500.0, 'remainingQuantity': 0.0, 'requestedDestination': 'AUTO', 'destinationLinkName': 'CDRG', 'price': 61.17, 'orderLegCollection': [{'orderLegType': 'EQUITY', 'legId': 1, 'instrument': {'assetType': 'EQUITY', 'cusip': '77543R102', 'symbol': 'ROKU'}, 'instruction': 'BUY', 'positionEffect': 'OPENING', 'quantity': 500.0}], 'orderStrategyType': 'SINGLE', 'orderId': 378977555, 'cancelable': False, 'editable': False, 'status': 'FILLED', 'enteredTime': '2018-08-29T14:33:40+0000', 'closeTime': '2018-08-29T14:33:40+0000', 'tag': 'WEB_GRID_SNAP', 'accountId': 425567337, 'orderActivityCollection': [{'activityType': 'EXECUTION', 'executionType': 'FILL', 'quantity': 500.0, 'orderRemainingQuantity': 0.0, 'executionLegs': [{'legId': 1, 'quantity': 500.0, 'mismarkedQuantity': 0.0, 'price': 61.156, 'time': '2018-08-29T14:33:40+0000'}]}]}, {'session': 'NORMAL', 'duration': 'DAY', 'orderType': 'MARKET', 'complexOrderStrategyType': 'NONE', 'quantity': 500.0, 'filledQuantity': 500.0, 'remainingQuantity': 0.0, 'requestedDestination': 'AUTO', 'destinationLinkName': 'SOHO', 'orderLegCollection': [{'orderLegType': 'EQUITY', 'legId': 1, 'instrument': {'assetType': 'EQUITY', 'cusip': '77543R102', 'symbol': 'ROKU'}, 'instruction': 'SELL', 'positionEffect': 'CLOSING', 'quantity': 500.0}], 'orderStrategyType': 'SINGLE', 'orderId': 378977459, 'cancelable': False, 'editable': False, 'status': 'FILLED', 'enteredTime': '2018-08-29T14:08:05+0000', 'closeTime': '2018-08-29T14:08:06+0000', 'tag': 'WEB_GRID_SNAP', 'accountId': 425567337, 'orderActivityCollection': [{'activityType': 'EXECUTION', 'executionType': 'FILL', 'quantity': 500.0, 'orderRemainingQuantity': 0.0, 'executionLegs': [{'legId': 1, 'quantity': 500.0, 'mismarkedQuantity': 0.0, 'price': 60.5143, 'time': '2018-08-29T14:08:06+0000'}]}]}, {'session': 'NORMAL', 'duration': 'DAY', 'orderType': 'MARKET', 'complexOrderStrategyType': 'NONE', 'quantity': 500.0, 'filledQuantity': 500.0, 'remainingQuantity': 0.0, 'requestedDestination': 'AUTO', 'destinationLinkName': 'CDRG', 'orderLegCollection': [{'orderLegType': 'EQUITY', 'legId': 1, 'instrument': {'assetType': 'EQUITY', 'cusip': '77543R102', 'symbol': 'ROKU'}, 'instruction': 'BUY', 'positionEffect': 'OPENING', 'quantity': 500.0}], 'orderStrategyType': 'SINGLE', 'orderId': 378977728, 'cancelable': False, 'editable': False, 'status': 'FILLED', 'enteredTime': '2018-08-29T15:20:28+0000', 'closeTime': '2018-08-29T15:20:28+0000', 'tag': 'WEB_GRID_SNAP', 'accountId': 425567337, 'orderActivityCollection': [{'activityType': 'EXECUTION', 'executionType': 'FILL', 'quantity': 500.0, 'orderRemainingQuantity': 0.0, 'executionLegs': [{'legId': 1, 'quantity': 500.0, 'mismarkedQuantity': 0.0, 'price': 60.9738, 'time': '2018-08-29T15:20:28+0000'}]}]}, {'session': 'NORMAL', 'duration': 'DAY', 'orderType': 'MARKET', 'complexOrderStrategyType': 'NONE', 'quantity': 500.0, 'filledQuantity': 500.0, 'remainingQuantity': 0.0, 'requestedDestination': 'AUTO', 'destinationLinkName': 'CDRG', 'orderLegCollection': [{'orderLegType': 'EQUITY', 'legId': 1, 'instrument': {'assetType': 'EQUITY', 'cusip': '77543R102', 'symbol': 'ROKU'}, 'instruction': 'SELL', 'positionEffect': 'CLOSING', 'quantity': 500.0}], 'orderStrategyType': 'SINGLE', 'orderId': 378977617, 'cancelable': False, 'editable': False, 'status': 'FILLED', 'enteredTime': '2018-08-29T14:53:14+0000', 'closeTime': '2018-08-29T14:53:14+0000', 'tag': 'WEB_GRID_SNAP', 'accountId': 425567337, 'orderActivityCollection': [{'activityType': 'EXECUTION', 'executionType': 'FILL', 'quantity': 200.0, 'orderRemainingQuantity': 300.0, 'executionLegs': [{'legId': 1, 'quantity': 200.0, 'mismarkedQuantity': 0.0, 'price': 61.436, 'time': '2018-08-29T14:53:14+0000'}]}, {'activityType': 'EXECUTION', 'executionType': 'FILL', 'quantity': 100.0, 'orderRemainingQuantity': 200.0, 'executionLegs': [{'legId': 1, 'quantity': 100.0, 'mismarkedQuantity': 0.0, 'price': 61.436, 'time': '2018-08-29T14:53:14+0000'}]}, {'activityType': 'EXECUTION', 'executionType': 'FILL', 'quantity': 100.0, 'orderRemainingQuantity': 100.0, 'executionLegs': [{'legId': 1, 'quantity': 100.0, 'mismarkedQuantity': 0.0, 'price': 61.436, 'time': '2018-08-29T14:53:14+0000'}]}, {'activityType': 'EXECUTION', 'executionType': 'FILL', 'quantity': 100.0, 'orderRemainingQuantity': 0.0, 'executionLegs': [{'legId': 1, 'quantity': 100.0, 'mismarkedQuantity': 0.0, 'price': 61.43, 'time': '2018-08-29T14:53:14+0000'}]}]}]

