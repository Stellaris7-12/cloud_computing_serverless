import pickle
import json

# Load the model
filename = 'iris_model.sav'
model = pickle.load(open(filename, 'rb'))

def predict(features):
    return model.predict(features).tolist()

def lambda_handler(event, context):
    """
    处理来自API Gateway的请求，进行IRIS花卉分类预测
    """
    try:
        # 1. 解析输入数据
        print("收到事件:", json.dumps(event))  # 用于调试
        
        # 从event中提取body（API Gateway会将HTTP请求体放在这里）
        if 'body' in event:
            # body可能是字符串形式的JSON，需要解析
            if isinstance(event['body'], str):
                body = json.loads(event['body'])
            else:
                body = event['body']
        else:
            # 如果没有body，直接使用event（可能是测试事件）
            body = event
        
        # 2. 提取特征值
        if 'values' in body:
            features = body['values']
        else:
            # 如果values不在顶层，尝试在body中查找
            features = body.get('values', [])
        
        # 3. 验证输入数据
        if not features:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': '缺少输入数据',
                    'message': '请在请求体中提供 "values" 字段，格式: {"values": [[f1, f2, f3, f4]]}'
                })
            }
        
        # 检查特征维度
        if not all(len(feature) == 4 for feature in features):
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': '输入格式错误',
                    'message': '每个特征数组必须包含4个数值: [sepal_length, sepal_width, petal_length, petal_width]'
                })
            }
        
        # 4. 调用预测函数
        print(f"进行预测，特征: {features}")  # 调试日志
        predictions = predict(features)
        print(f"预测结果: {predictions}")  # 调试日志
        
        # 5. 构建响应
        response = {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # 允许CORS，便于前端调用
            },
            'body': json.dumps({
                'predictions': predictions,
                'input_features': features,
                'message': '预测成功'
            })
        }
        
        return response
        
    except json.JSONDecodeError as e:
        # JSON解析错误
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'JSON解析错误',
                'message': f'请求体必须是有效的JSON: {str(e)}'
            })
        }
    except Exception as e:
        # 其他所有错误
        print(f"处理请求时发生错误: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': '内部服务器错误',
                'message': f'预测过程中发生错误: {str(e)}'
            })
        }