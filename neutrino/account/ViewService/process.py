
from .exception import InsertionServerError
from django.db.models import Model
from django.core.validators import RegexValidator

check_regex = lambda regex , message : RegexValidator(regex=regex , message=message , code='invalid_regex')
# get from settings 
access_field_name  = True 
_valid_param_regex = r'^[a-zA-Z0-9_,]+$'


class BaseQuerySetSerializer:
    model_base = None
     
    def rasie_None_error(self , NONE:None)->None:
        raise NotImplementedError(f'you have to import fields in query Param \n  not be None ... ')

    def __init__(self , **kwargs):
        print('the query from server' , kwargs.get('query_param') , type(kwargs.get('query_param')))
        assert kwargs.get('query_param') , InsertionServerError('Don`t Valid insertion from Query_Param') # check 
        query_set_kwargs = kwargs['query_param'].get('fields') if kwargs.get('query_param').get('fields') else self.rasie_None_error(None)
        self._validated_fields = [] # why i dont use get because for implamnet maynot base none befor that rasie dont exist index error 
        self.run_validation(query_set_kwargs)

    @property
    def model(self) -> Model :
        assert self.model_base , 'You must to add the model_base'
        return self.model_base 


    def _get_Field_names(self)->dict:
        return self.model.__dict__  if access_field_name else ''


    def check_field_in_model(self , field:str)->None: 
        print('field is ' , field)
        assert isinstance(field , str)  , f"Field insertion must be __str__ not {type(field)} such Type"
        print("the model is" , self.model)
        assert hasattr(self.model , str(field)) , InsertionServerError(f'Field Database Error this field is not requried in \n \'{self._get_Field_names()}\'')
    
    
    def run_validation(self , Query_data_str:str)->None:
        #'?fileds['parsa' , 'sepehr' , zahra]'
        print('the  Query Data is '  , Query_data_str)
        self._valid_query_param = Query_data_str.split(',')
        print('validate query param is ' , self._valid_query_param)
        if (Query_data_str.count(',') + 1 == len(self._valid_query_param)) or (Query_data_str.count(',') == len(self._valid_query_param)) :
            print('pass the Query dict statu')
            check_regex(_valid_param_regex , "The QueryParam dont allow Regex")(Query_data_str)

        
        else : 
            assert False , InsertionServerError(f'invald queryParam \n  \'{Query_data_str}')
        
        
        print('the all Query set in validation is ' ,Query_data_str)
        for field in self._valid_query_param:
            print(f'checking  {field}')
            self.check_field_in_model(field)
            if field not in self._validated_fields : 
                self._validated_fields.append(str(field))
            else : 
                continue

    @property
    def data(self)->tuple:
        # assert hasattr(self , '_run_validation') , "you must to run validation \n before get data" # TODO rm checking  becuase run vaidation call in __init__ 
        return tuple(self._validated_fields)
    
        


