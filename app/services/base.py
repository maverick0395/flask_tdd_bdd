from http.client import HTTPException
from typing import Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.sql.elements import BinaryExpression

from app import db
from app.logger import log


ModelType = TypeVar("ModelType", bound=db.Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
GetSchemaType = TypeVar("GetSchemaType", bound=BaseModel)
QuerySchemaType = TypeVar("QuerySchemaType", bound=BaseModel)


class BaseService:
    model: Type[ModelType]
    create_schema: CreateSchemaType
    update_schema: UpdateSchemaType
    get_schema: GetSchemaType
    query_schema: QuerySchemaType


    def commit(self) -> None:
        """Commits the current transaction to the database"""
        try:
            db.session.commit()
        except Exception as error:
            raise error


    def create(self, schema: BaseModel, **kwargs: dict) -> ModelType:
        """
        Adds new record to the table.

        Parameters
        ----------
            schema : BaseModel
                object with data to create record item from
            kwargs : dict
                dictionary with an arbitrary number of keyword arguments

        Returns
        ----------
            model type instance
        """
        try:
            instance: self.model = self.model(**schema.dict(exclude_unset=True), **kwargs)
            db.session.add(instance)
            self.commit()
            log(log.INFO, "Item %s has been created", instance)
            return instance
        except Exception as error:
            raise error


    def delete(self, **kwargs) -> None:
        """
        Deletes a record from the table.

        Parameters
        ----------
            kwargs : dict
                dictionary with an arbitrary number of keyword arguments
        """
        try:
            instance: self.model = self.model.query.filter_by(**kwargs).delete()
            if not instance:
                raise HTTPException(status_code=404, detail="Object does not exist")
            self.commit()
            log(log.INFO, "Item %s has been deleted", instance)
        except Exception as error:
            raise error


    def delete_all(self, model: ModelType) -> None:
        """
        Deletes all records from the table.

        Parameters
        ----------
            model : ModelType
                model to delete all records from
        """
        try:
            db.session.query(model).delete()
            self.commit()
            log(log.INFO, "All %s`s records has been deleted", model)
        except Exception as error:
            raise error


    def get(self, **kwargs) -> Optional[GetSchemaType]:
        """
        Gets record from the table.

        Parameters
        ----------
            kwargs : dict
                dictionary with an arbitrary number of keyword arguments

        Returns
        ---------
            first record from query result
        """
        try:
            return self.model.query.filter_by(**kwargs).first()
        except Exception as error:
            raise error


    def get_all(self) -> list[GetSchemaType]:
        """
        Select all from table.

        Returns
        -------
            list of table`s records
        """
        try:
            return self.model.query.all()
        except Exception as error:
            raise error


    def get_all_by_multiple_filters(
        self, filter_query: BinaryExpression, **kwargs
    ) -> list[GetSchemaType]:
        """
        Select all by binary expression query from table.

        Returns
        -------
            list of table`s records
        """
        try:
            return self.model.query.filter_by(**kwargs).filter(filter_query).all()
        except Exception as error:
            raise error


    def get_all_by_filter_query(self, **kwargs) -> list[GetSchemaType]:
        """
        Select all by filter query from table.

        Returns
        -------
            list of table`s records
        """
        try:
            return self.model.query.filter_by(**kwargs).all()
        except Exception as error:
            raise error


    def get_first(self) -> Optional[GetSchemaType]:
        """
        Gets first record from the table.

        Returns
        ---------
            first record from query result
        """
        try:
            return self.model.query.first()
        except Exception as error:
            raise error


    def update(self, id: int, **kwargs) -> None:
        """
        Updates a record in the table.

        Parameters
        ----------
            id : int
                table`s record id value to filter by
            kwargs : dict
                dictionary with an arbitrary number of keyword arguments

        """
        try:
            instance: self.model = self.model.query.filter_by(id=id).all()[0]
            for attr, new_value in kwargs.items():
                setattr(instance, attr, new_value)
            self.commit()
            log(log.INFO, "Item %s has been updated", instance)
        except Exception as error:
            raise error
