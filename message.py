class Message:
    ERROR_ARGUMENTS_LIST_FORMAT = '參數錯誤，請查詢說明網站資料'
    ERROR_AUTHTOKEN_NOT_SUPPORTED = ''
    ERROR_COLUMNS_DATA_NOT_MATCHED = '欄位數量不一致'

    WARN_DATA_LIMIT_EXCEEDED = '本次呼叫已超過 tejapi.get() 允許的資料筆數，請增加篩選條件減少筆數或採用其他方法取得資料. ' 
    WARN_PAGE_LIMIT_EXCEEDED = '如需要更多資料，請設定參數 paginate=True，詳細訊息: %s '
    WARN_PARAMS_NOT_SUPPORTED = '%s will no longer supported. Please use %s instead'
